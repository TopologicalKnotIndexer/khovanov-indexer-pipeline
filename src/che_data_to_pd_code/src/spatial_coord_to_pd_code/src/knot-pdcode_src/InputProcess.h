#pragma once

#include <cassert>
#include <cstdio>
#include <vector>
#include "Vector3d.h"

typedef std::vector<Vector3d> PointList;

struct InputData {
    PointList point_list;

    void debugOutput() const { // 输出调试用的辅助信息
        printf("%d\n", (int)point_list.size());

        for(int i = 0; i < point_list.size(); i += 1) {
            point_list[i].debugOutput();
        }
    }

    void getSegment(int index, Vector3d& pFrom, Vector3d& pTo) const {
        assert(0 <= index && index < (int)this->point_list.size());

        int now_index = index;
        int nxt_index = (index + 1) % (int)this->point_list.size();

        pFrom = this->point_list[now_index];
        pTo   = this->point_list[nxt_index]; // 获取第 index 段线段的 from 和 to
    }

    Vector3d getSegmentPos(int index, double t) const {
        assert(0 <= t && t <= 1);

        Vector3d pFrom(0, 0, 0), pTo(0, 0, 0); // 获取线段端点
        this->getSegment(index, pFrom, pTo);
        return this->getSegmentPoint(pFrom, pTo, t); // 获取线段上某个位置的点
    }

    // 在线段上获取一个指定参数位置的点
    Vector3d getSegmentPoint(const Vector3d& pFrom, const Vector3d& pTo, double t) const {
        assert(0 <= t && t <= 1);

        Vector3d v = pTo; // v = (pTo - pFrom) * t
        v.sub(pFrom);
        v.multiply(t);

        Vector3d p = pFrom; // p = pFrom + v
        p.add(v);
        return p;
    }

    void multiply(double multiple) { // 成比例放大坐标
        for(auto& vector3d: this->point_list) {
            vector3d.multiply(multiple);
        }
    }
};

class InputProcess {
public:
    InputProcess() {}

    virtual int getInt() { // 读取一个整数
        int val;
        scanf("%d", &val);
        return val;
    }

    virtual double getDouble() { // 读取一个浮点数
        double val;
        scanf("%lf", &val);
        return val;
    }

    inline void run(InputData& p_input_data) { // 运行输入程序
        p_input_data.point_list.clear();
        int n = this->getInt();

        for(int i = 0; i < n; i += 1) {
            double pX, pY, pZ;
            pX = this->getDouble();
            pY = this->getDouble();
            pZ = this->getDouble();

            // 向输入序列中追加元素
            p_input_data.point_list.push_back(Vector3d(pX, pY, pZ));
        }
    }
};