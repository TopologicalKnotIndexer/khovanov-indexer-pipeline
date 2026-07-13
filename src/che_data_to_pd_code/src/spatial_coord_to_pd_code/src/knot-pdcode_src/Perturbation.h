#pragma once

#include "InputProcess.h"
#include "RandDir.h"

class Perturbation { // 对所有点坐标进行扰动
public:
    Perturbation() {}

    virtual void pertubate(InputData& input_data, double max_d) { // 对输入的所有点坐标进行合理的扰动
        // 我们假设所有扰动都只在 x, y 两个维度进行
        RandDir& rand_dir = RandDir::getInstance();

        for(int i = 0; i < input_data.point_list.size(); i += 1) {
            // 获取一个 x, y 平面中的随机方向单位向量
            Vector3d v3d = rand_dir.getRandomUnitVector3d();
            v3d.getZ() = 0;
            v3d.unify();

            v3d.multiply(max_d);                // 按照比例缩放得到一个最大偏移
            v3d.multiply(rand_dir.getRandom()); // 随机一个实际偏移比例

            input_data.point_list[i].add(v3d); // 叠加一个随机扰动
        }
    }
};