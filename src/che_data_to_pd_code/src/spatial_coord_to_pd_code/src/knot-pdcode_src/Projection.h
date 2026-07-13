#pragma once

#include "InputProcess.h"
#include "RandDir.h"

class Projection { // 把点向量在某个方向上做投影
public:
    Projection() {}

    // norm 是投影平面的法向量
    virtual void project(InputData& input_data, Vector3d norm) { // 把输入的所有坐标在某个方向上做投影
        Vector3d vx(0, 0, 0), vy(0, 0, 0);
        RandDir& rand_dir = RandDir::getInstance(); // 获取单例

        rand_dir.getVectorBasis(norm, vx, vy);
        for(int i = 0; i < input_data.point_list.size(); i += 1) { // 根据新的坐标系重新计算 x, y, z
            double nx = input_data.point_list[i].dot(vx);
            double ny = input_data.point_list[i].dot(vy);
            double nz = input_data.point_list[i].dot(norm);

            input_data.point_list[i] = Vector3d(nx, ny, nz); // 得到新的点坐标
        }
    }

    virtual double getOriginalVector2dDistance(const InputData& input_data) {
        double ans_dis = 1e300;
        for(int i = 0; i < input_data.point_list.size(); i += 1) {
            for(int j = i + 1; j < input_data.point_list.size(); j += 1) {
                Vector2d vf = input_data.point_list[i].getVector2d();
                Vector2d vt = input_data.point_list[j].getVector2d();
                vt.sub(vf); // 计算二维空间中的距离
                ans_dis = std::min(ans_dis, vt.getLength());
            }
        }
        return ans_dis;
    }
};