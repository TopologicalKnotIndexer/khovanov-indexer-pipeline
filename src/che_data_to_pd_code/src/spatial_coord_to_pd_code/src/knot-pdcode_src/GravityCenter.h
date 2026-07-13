#pragma once // 计算重心

#include <cassert>
#include "Vector3d.h"
#include "InputProcess.h"

class GravityCenter {
public:
    GravityCenter() {}

    virtual Vector3d getGravityCenter(const InputData& input_data) { // 求重心
        assert(input_data.point_list.size() > 0);
        Vector3d ans(0, 0, 0);

        for(int i = 0; i < input_data.point_list.size(); i += 1) {
            ans.add(input_data.point_list[i]);
        }

        ans.multiply(1.0 / (double)input_data.point_list.size());
        return ans;
    }

    virtual void moveInputData(InputData& input_data) { // 将坐标原点移动到重心
        Vector3d gravity_center = this->getGravityCenter(input_data);

        for(int i = 0; i < input_data.point_list.size(); i += 1) {
            input_data.point_list[i].sub(gravity_center);
        }
    }

    virtual void multiplyInputData(InputData& input_data, double mul) { // 坐标按比例放大
        assert(mul > 0);

        for(int i = 0; i < input_data.point_list.size(); i += 1) {
            input_data.point_list[i].multiply(mul);
        }
    }
};