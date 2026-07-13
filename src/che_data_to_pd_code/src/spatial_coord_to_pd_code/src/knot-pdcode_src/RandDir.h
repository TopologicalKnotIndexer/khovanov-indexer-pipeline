#pragma once

#include <cassert>
#include <cmath>
#include <cstdlib>
#include <ctime>

#include "Vector3d.h"

class RandDir { // 生成一个随机方向的单位向量
private:
    RandDir() {
        srand(time(NULL));
    }
    const double epsilon = 1e-12; // 精度误差系数

public:
    static RandDir& getInstance() { // 获取单例
        static RandDir* rand_dir = nullptr;

        if(rand_dir == nullptr) {
            rand_dir = new RandDir();
        }
        return *rand_dir;
    }

    int getRandint() { // 获得一个随机整数
        if(RAND_MAX > 0x7fff) {
            return rand();
        }else {
            long long val = ((long long)rand()   << 15) | rand(); // 兼容 windows 操作系统
            return val;
        }
    }

    double getRandom() { // 获取 0 ~ 1 之间的随机数
        if(RAND_MAX > 0x7fff) {
            return (double)rand() / RAND_MAX;
        }else {
            long long val = ((long long)rand()   << 15) | rand(); // 兼容 windows 操作系统
            long long rmx = ((long long)RAND_MAX << 15) | RAND_MAX;
            return (double)val / rmx;
        }
    }

    Vector3d getRandomUnitVector3d() {
        Vector3d ans(this->getRandom(), this->getRandom(), this->getRandom());

        while(ans.getLength() > 1.0) { // 保证生成的过程是等概率的
            ans.getX() = this->getRandom();
            ans.getY() = this->getRandom();
            ans.getZ() = this->getRandom();
        }
        double length = ans.getLength();

        ans.unify();
        return ans; // 使用默认拷贝构造函数
    }

    Vector3d getRandomNormVector3d(const Vector3d& vector_3d) {  // 计算一个随机的与给定向量垂直的向量
        assert(fabs(vector_3d.getLength() - 1) < this->epsilon); // 输入向量必须是单位向量

        Vector3d rand_vec = getRandomUnitVector3d();
        while(1 - fabs(rand_vec.dot(vector_3d)) <= this->epsilon) { // 方向过于接近
            rand_vec = getRandomUnitVector3d();
        }

        double project = rand_vec.dot(vector_3d);
        Vector3d resize_norm = vector_3d;
        resize_norm.multiply(project); // 得到 rand_vec 在 vector_3d 上的投影向量
        
        rand_vec.sub(resize_norm); // 剪掉投影向量，剩下的部分再单位化
        rand_vec.unify();
        return rand_vec; // 得到一个和原始向量垂直的向量
    }

    void getVectorBasis(const Vector3d& norm, Vector3d& vx, Vector3d& vy) { // 根据 norm 构建一组随机基底 {norm, x, y}
        assert(fabs(norm.getLength() - 1) < this->epsilon); // 输入向量必须是单位向量

        vx = this->getRandomNormVector3d(norm); // 获得一个随机的垂直向量
        vy = Vector3d::cross(norm, vx);         // 叉积获得另一个垂直向量
        vy.unify();
    }
};