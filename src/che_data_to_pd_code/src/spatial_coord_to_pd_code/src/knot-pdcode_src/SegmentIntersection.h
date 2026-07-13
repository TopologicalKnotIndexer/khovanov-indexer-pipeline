#pragma once

#include <algorithm>
#include <cassert>
#include <cmath>
#include <vector>
#include "Vector3d.h"
#include "InputProcess.h"
typedef std::vector<Vector2d> Vector2dList; // 记录二维坐标集合

struct IntersectionInfo {
    int    segment_id;   // from 0 to n-1
    double t_in_segment; // (0, 1)
    int    uuid;         // 在二维平面上重合的两个点具有相同的 uuid

    IntersectionInfo(int p_segment_id, double p_t_in_segment, int p_uuid): 
        segment_id(p_segment_id), t_in_segment(p_t_in_segment), uuid(p_uuid) {}
};
typedef std::vector<IntersectionInfo> RawIntersectionInfoList; // 用来记录所有的交点信息
struct IntersectionInfoList {
    RawIntersectionInfoList raw_intersection_info_list;

    void debugOutput() {
        int n = (int)this->raw_intersection_info_list.size();
        printf("%d\n", n);

        for(int i = 0; i < n; i += 1) {
            IntersectionInfo& ii = this->raw_intersection_info_list[i];
            printf("%5d %27.17lf (%3d)\n", ii.segment_id, ii.t_in_segment, ii.uuid);
        }
    }
};

class SegmentIntersection {
private:
    const double epsilon = 1e-12;

    double getInterCross(Vector2d a, Vector2d f, Vector2d t) { // 考虑 a 在线段 f -> t 的哪一侧
        a.sub(f);
        t.sub(f);
        return Vector2d::cross(a, t);
    }

    static bool intersectionInfoCmp(const IntersectionInfo& ii1, const IntersectionInfo& ii2) {
        if(ii1.segment_id != ii2.segment_id) {
            return ii1.segment_id < ii2.segment_id; // 以线段编号为第一关键字，线段中的参数为第二关键字排序
        }
        return ii1.t_in_segment < ii2.t_in_segment;
    }

public:
    SegmentIntersection() {};

    // 两条线段分别为 vf1 -> vt1 和 vf2 -> vt2
    // 假设两条线段没有公共端点
    bool hasIntersection(Vector2d vf1, Vector2d vt1, Vector2d vf2, Vector2d vt2) { // 判断两条线段是否有交点
        double side_vf1 = this->getInterCross(vf1, vf2, vt2);
        double side_vt1 = this->getInterCross(vt1, vf2, vt2);
        double side_vf2 = this->getInterCross(vf2, vf1, vt1);
        double side_vt2 = this->getInterCross(vt2, vf1, vt1);

        return side_vf1*side_vt1 < -this->epsilon && side_vf2*side_vt2 < -this->epsilon; // 判断线段是否相交
    }

    // 解方程
    // A1x + B1y = C1
    // A2x + B2y = C2
    void getSolution(double A1, double B1, double C1, double A2, double B2, double C2, double& x, double& y) {
        double base = A1 * B2 - A2 * B1;
        assert(fabs(base) > this->epsilon);

        x = (C1 * B2 - C2 * B1) / base;
        y = (A1 * C2 - A2 * C1) / base; // 解方程组
    }

    // 获取交点在两条线段上各自的参数坐标（介于 0 ~ 1）之间
    void getIntersection(Vector2d vf1, Vector2d vt1, Vector2d vf2, Vector2d vt2, double& t1, double& t2) {
        assert(this->hasIntersection(vf1, vt1, vf2, vt2)); // 没有交点不要求交点

        Vector2d v1 = vt1; // v1 = vt1 - vf1
        v1.sub(vf1);

        Vector2d v2 = vt2; // v2 = vt2 - vf2
        v2.sub(vf2);

        // 解方程求出两侧的参数
        this->getSolution(-v1.getX(), v2.getX(), vf1.getX()-vf2.getX(), -v1.getY(), v2.getY(), vf1.getY()-vf2.getY(), t1, t2);
    }

    Vector2d getVector2dIntersection(Vector2d vf1_2d, Vector2d vt1_2d, double t1) {
        Vector2d v = vt1_2d; v.sub(vf1_2d); v.multiply(t1); // v = t1 * (t - f)
        Vector2d b = vf1_2d; b.add(v);                      // b = f + v
        return b;
    }

    void getAllIntersectionIn2d(const InputData& input_data, IntersectionInfoList& intersection_info_list, Vector2dList& vector2d_list) {
        RawIntersectionInfoList& raw_intersection_info_list = intersection_info_list.raw_intersection_info_list;
        const PointList& point_list = input_data.point_list;
        const int n                 = (int)point_list.size();

        raw_intersection_info_list.clear();
        vector2d_list.clear(); // 用来记录所有的投影后的交点的二维坐标
        int uuid = 0;          // 用来标识实际上相互重合的两个节点

        for(int i = 0; i < n; i += 1) {
            for(int j = 0; j < n; j += 1) {
                int lst = (i + n - 1) % n;
                int nxt = (i + 1) % n; // 我们要求 i 和 j 不能为相邻线段，相邻线段之间不需要求交

                if(j != lst && j != i && j != nxt && i < j) {
                    Vector3d vf1(0, 0, 0), vt1(0, 0, 0); // 先获取线段端点，再判交，再记录交点信息
                    Vector3d vf2(0, 0, 0), vt2(0, 0, 0);
                    input_data.getSegment(i, vf1, vt1);
                    input_data.getSegment(j, vf2, vt2);

                    Vector2d vf1_2d = vf1.getVector2d(); // 获得 2d 投影
                    Vector2d vt1_2d = vt1.getVector2d();
                    Vector2d vf2_2d = vf2.getVector2d();
                    Vector2d vt2_2d = vt2.getVector2d();

                    if(this->hasIntersection(vf1_2d, vt1_2d, vf2_2d, vt2_2d)) {
                        double t1, t2;
                        this->getIntersection(vf1_2d, vt1_2d, vf2_2d, vt2_2d, t1, t2);

                        ++ uuid; // 记录新的交点信息
                        raw_intersection_info_list.push_back(IntersectionInfo(i, t1, uuid));
                        raw_intersection_info_list.push_back(IntersectionInfo(j, t2, uuid));

                        // 记录新交点坐标
                        vector2d_list.push_back(getVector2dIntersection(vf1_2d, vt1_2d, t1));
                    }
                }
            }
        }

        // 对所有交点信息进行排序
        std::sort(raw_intersection_info_list.begin(), raw_intersection_info_list.end(), SegmentIntersection::intersectionInfoCmp);
    }

    double getMinPointDistance(const Vector2dList& vector2d_list) const { // 计算最小距离
        double ans = 1e300;
        for(int i = 0; i < vector2d_list.size(); i += 1) {
            for(int j = i + 1; j < vector2d_list.size(); j += 1) {
                Vector2d v = vector2d_list[i]; // 计算两个点之间的距离
                v.sub(vector2d_list[j]);
                ans = std::min(ans, v.getLength());
            }
        }
        return ans;
    }
};
