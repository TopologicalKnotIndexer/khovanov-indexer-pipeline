#pragma once

#include <algorithm>
#include <vector>
#include <string>
#include <sstream>
#include "InputProcess.h"
#include "SegmentIntersection.h"

struct PDcode {
    int a[4];

    PDcode() {
        for(int i = 0; i < 4; i += 1) {
            a[i] = 0;
        }
    }

    PDcode(const std::vector<int>& code_arr) {
        assert(code_arr.size() == 4);

        for(int i = 0; i < (int)code_arr.size(); i += 1) {
            a[i] = code_arr[i];
        }
    }

    std::string getString(bool compact=false) const { // 获取字符串表示
        std::string ans = (compact ? "" : "X");
        ans += "[";

        for(int i = 0; i < 4; i += 1) {
            ans += std::to_string(a[i]);

            if(i != 3) {
                ans += ", "; // 创建分隔符
            }
        }

        ans += "]";
        return ans;
    }

    void debugOutput(bool need_new_line=true) const {
        printf("%s", this->getString().c_str());

        if(need_new_line) { // 如果需要换行则输出，默认需要
            printf("\n");
        }
    }
};
typedef std::vector<PDcode> RawPDcodeList;
struct PDcodeList {
    RawPDcodeList raw_pd_code_list;
    PDcodeList() {}

    PDcodeList(const std::vector<std::vector<int>> const_arr) {
        for(int i = 0; i < const_arr.size(); i += 1) {
            assert(const_arr[i].size() == 4);

            raw_pd_code_list.push_back(PDcode(const_arr[i])); // 构造 PDcode 序列
        }
    }

    void debugOutput(bool compact=false) const {
        printf("%s\n", getString(compact).c_str());
    }

    std::string getString(bool compact=false) const { // 生成字符串形式的 PDcode
        std::string ans = (compact ? "" : "PD");
        ans += "[";

        for(int i = 0; i < raw_pd_code_list.size(); i += 1) {
            ans += raw_pd_code_list[i].getString(compact);

            if(i != raw_pd_code_list.size() - 1) {
                ans += ", ";
            }
        }

        ans += "]";
        return ans;
    }

    void loadFromString(std::string pd_code_string) { // 从字符串加载 pd_code
        // 只保留与数值相关的部分
        for(int i = 0; i < pd_code_string.size(); i += 1) {
            if(pd_code_string[i] < '0' || pd_code_string[i] > '9') pd_code_string[i] = ' ';
        }

        std::vector<int> int_list;
        std::vector<std::vector<int> > pre_pd_code;
        std::stringstream ss;
        ss << pd_code_string;

        int index; // 读取所有数据
        while(ss >> index) {
            int_list.push_back(index);
        }
        assert(int_list.size() % 4 == 0);

        for(int i = 0; i < int_list.size(); i += 4) {
            std::vector<int> arr;
            for(int j = 0; j < 4; j += 1) {
                int val = i + j;
                arr.push_back(int_list[val]);
            }
            pre_pd_code.push_back(arr);
        }
        (*this) = PDcodeList(pre_pd_code);
    }
};

class PDcodeGenerator {
private:
    struct ToolNode {       // 用于排序的工具结构体
        bool   is_first;    // 是否是第一条即下方入边
        int    relevant_id; // 与之关联的边 id
        double rad;         // 向量辐角
    };
    typedef std::vector<ToolNode> ToolNodeList;

    static bool toolNodeCmp(ToolNode tn1, ToolNode tn2) {
        return tn1.rad > tn2.rad; // 顺时针给出
    }

    static bool pDcodeCmp(PDcode pd1, PDcode pd2) { // 用于给 pd_code 排序
        for(int i = 0; i < 4; i += 1) {
            if(pd1.a[i] != pd2.a[i]) {
                return pd1.a[i] < pd2.a[i];
            }
        }
        return true;
    }

public:
    PDcodeGenerator() {}

    virtual PDcode getPDcode(
        Vector2d left_1_2d, Vector2d right_1_2d, int left_id_1, int right_id_1, Vector3d cross_1,
        Vector2d left_2_2d, Vector2d right_2_2d, int left_id_2, int right_id_2, Vector3d cross_2) {

        if(cross_1.getZ() > cross_2.getZ()) { // 保证 cross_1 在 cross_2 下面
            std::swap( left_1_2d,  left_2_2d);
            std::swap(right_1_2d, right_2_2d);
            std::swap( left_id_1,  left_id_2);
            std::swap(right_id_1, right_id_2);
            std::swap(   cross_1,    cross_2); // 交换两个节点的全部信息
        }

        Vector2d cross = cross_1.getVector2d(); // 获取二维投影下的交点坐标
        left_1_2d .sub(cross);
        left_2_2d .sub(cross);
        right_1_2d.sub(cross);
        right_2_2d.sub(cross); // 计算相对于交叉点的相对坐标

        ToolNodeList tool_node_list;
        tool_node_list.push_back((ToolNode){ true,  left_id_1,  left_1_2d.calculateAngle()});
        tool_node_list.push_back((ToolNode){false,  left_id_2,  left_2_2d.calculateAngle()});
        tool_node_list.push_back((ToolNode){false, right_id_1, right_1_2d.calculateAngle()});
        tool_node_list.push_back((ToolNode){false, right_id_2, right_2_2d.calculateAngle()});

        // 按照辐角从大到小排序
        std::sort(tool_node_list.begin(), tool_node_list.end(), PDcodeGenerator::toolNodeCmp);
        int index = 0;
        while(!tool_node_list[index].is_first) { // 找到起始位置
            index += 1;
        }

        PDcode ans;
        for(int i = 0; i < 4; i += 1) { // 从第一条边开始逆时针往里加
            int pos = (index + i) % 4;
            ans.a[i] = tool_node_list[pos].relevant_id;
        }
        return ans;
    }

    virtual void generate(
        const InputData& input_data, 
        const IntersectionInfoList& intersection_info_list,
        PDcodeList& pd_code_list) {

        RawPDcodeList& raw_pd_code_list = pd_code_list.raw_pd_code_list;
        raw_pd_code_list.clear(); // 清空 PD code 序列
        const RawIntersectionInfoList& raw_intersection_info_list = intersection_info_list.raw_intersection_info_list;

        const int n = raw_intersection_info_list.size(); // 段的个数
        for(int i = 0; i < n; i += 1) {
            for(int j = i + 1; j < n; j += 1) {

                // 检测重合的交点
                if(raw_intersection_info_list[i].uuid == raw_intersection_info_list[j].uuid) {
                    int   seg_id1 = raw_intersection_info_list[i].segment_id;
                    int   seg_id2 = raw_intersection_info_list[j].segment_id;
                    double seg_t1 = raw_intersection_info_list[i].t_in_segment;
                    double seg_t2 = raw_intersection_info_list[j].t_in_segment;

                    Vector2d left_1_2d  = input_data.getSegmentPos(seg_id1, seg_t1 / 2).getVector2d();
                    Vector2d left_2_2d  = input_data.getSegmentPos(seg_id2, seg_t2 / 2).getVector2d();
                    Vector2d right_1_2d = input_data.getSegmentPos(seg_id1, (1 + seg_t1) / 2).getVector2d();
                    Vector2d right_2_2d = input_data.getSegmentPos(seg_id2, (1 + seg_t2) / 2).getVector2d();

                    int left_id_1  = i;
                    int left_id_2  = j;
                    int right_id_1 = (i + 1) % n;
                    int right_id_2 = (j + 1) % n;

                    Vector3d cross_1 = input_data.getSegmentPos(seg_id1, seg_t1);
                    Vector3d cross_2 = input_data.getSegmentPos(seg_id2, seg_t2);

                    PDcode pd_code = this->getPDcode(
                        left_1_2d, right_1_2d, left_id_1 + 1, right_id_1 + 1, cross_1,
                        left_2_2d, right_2_2d, left_id_2 + 1, right_id_2 + 1, cross_2
                    );
                    raw_pd_code_list.push_back(pd_code); // 新增一个节点
                }
            }
        }

        std::sort(raw_pd_code_list.begin(), raw_pd_code_list.end(), PDcodeGenerator::pDcodeCmp);
    }
};