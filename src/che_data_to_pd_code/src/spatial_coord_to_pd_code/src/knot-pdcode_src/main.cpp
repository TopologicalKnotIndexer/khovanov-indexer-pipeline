#include <cstdio>

// 目前可用的下游选项
// http://katlas.org/wiki/The_Mathematica_Package_KnotTheory%60
// https://knotinfo.math.indiana.edu/index3.php
// sage

#include "GravityCenter.h"
#include "InputProcess.h"
#include "Perturbation.h"
#include "Projection.h"
#include "PDcodeGenerator.h"
#include "RandDir.h"
#include "SegmentIntersection.h"

#define KNOT_PDCODE_MAIN // 这里说明我们现在正在编译 KNOT_PDCODE 的程序
//#include "SageInterface.h"

#define COMPACT_PD_ONLY // 只输出一个 compact 风格的 pd_code

void test() {
    SegmentIntersection segment_intersection;
    Vector2d vf1(1.161260977510100378395918596652, -0.802651870706538761446324770077);
    Vector2d vt1(1.424805153451410344445093869581, -0.695334740693750674722650728654);
    Vector2d vf2(1.309320531565236311877242769697, -0.833843145325439683013257763378);
    Vector2d vt2(1.265584797266849026442514514201, -0.551443962657876429744874258176);

    printf("has = %d\n", segment_intersection.hasIntersection(vf1, vt1, vf2, vt2));

    double t1, t2;
    segment_intersection.getIntersection(vf1, vt1, vf2, vt2, t1, t2);
    printf("%25.17lf %25.17lf\n", t1, t2);
}

long long mysqr(long long x) { // Square without overflowing at 32-bit integer sizes.
    return x * x;
}

int main(int argc, char **argv) {
    // test();
    InputData            input_data;
    InputProcess         input_process;
    GravityCenter        gravity_center;
    Projection           projection;
    RandDir&             rand_dir       = RandDir::getInstance();
    Vector2dList         projection_points_list;
    Perturbation         pertubation;
    SegmentIntersection  segment_intersection;
    IntersectionInfoList intersection_info_list;
    PDcodeGenerator      pd_code_generator;
    PDcodeList           pd_code_list; // 存储计算得到的 pd code
    PDcodeList           pd_code_list_ans;
    //SageInterface        sage_interface(argv[0]); // 获得可执行文件路径
    const double         CURRENT_EPS = 1e-6;      // 这个 1e-6 将来一定要被替换成一个算法的输出

    input_process         .run                   (input_data);
    gravity_center        .moveInputData         (input_data);
    auto raw_input_data = input_data;           // 存档原始数据，每次重新拷贝这一输入

    // 控制次数
    const long long MAX_ATTEMPTS =
        std::max(1ll, (long long)(1e7) / mysqr((long long)raw_input_data.point_list.size())) + 1;
    for(long long attempt = 0; attempt < MAX_ATTEMPTS; attempt += 1) {
        if(input_data.point_list.size() <= 3) { // 小于等于三个点只可能构成平凡结
            printf("[]\n");
            return 0;
        }
        input_data              = raw_input_data;                                 // 拷贝原始数据
        Vector3d rand_direction = rand_dir.getRandomUnitVector3d();               // 每次投影前要随机选择投影方向
        projection.project(input_data, rand_direction);                           // 向随机方向进行投影
        
        double original_dis = projection.getOriginalVector2dDistance(input_data); // 计算初始的最小投影距离
        if(original_dis < 2.1 * CURRENT_EPS) {                                    // 保证初始时没有两点重合
            continue;
        }

        pertubation           .pertubate             (input_data, CURRENT_EPS); 
        segment_intersection  .getAllIntersectionIn2d(input_data, intersection_info_list, projection_points_list);

        double min_dis = segment_intersection.getMinPointDistance(projection_points_list);
        if(min_dis < 2 * CURRENT_EPS) { // 保证终止时没有三线共点
            continue;                   // 如果存在两点重合，那就重新计算投影
        }
        pd_code_generator     .generate              (input_data, intersection_info_list, pd_code_list);

        if(pd_code_list_ans.raw_pd_code_list.size() == 0 || pd_code_list.raw_pd_code_list.size() < pd_code_list_ans.raw_pd_code_list.size()) {
            pd_code_list_ans = pd_code_list;
        }
    }

    if(pd_code_list_ans.raw_pd_code_list.size() == 0) {
        fprintf(stderr, "ERROR: no regular projection found after %lld attempts.\n", MAX_ATTEMPTS);
        return 1;
    }

    //fprintf(stderr, "[DEBUG] pd_Code: len = %d\n", (int)pd_code_list_ans.raw_pd_code_list.size());

#ifdef COMPACT_PD_ONLY 
    pd_code_list_ans       .debugOutput           (true); //只输出一个紧致风格的 PD_CODE
#else
    pd_code_list_ans      .debugOutput           ();
    sage_interface        .debugOutput           (pd_code_list_ans);
#endif

    return 0;
}
