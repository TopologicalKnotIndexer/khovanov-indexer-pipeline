# 从命令行参数获取一个参数作为输入文件名
# 输出预测到的扭结类型到标准输出
import sys
from khovanov_indexer_pipeline import khovanov_indexer_pipeline

def main():
    assert len(sys.argv) == 2
    filename = sys.argv[1]
    for knotname in khovanov_indexer_pipeline(filename):
        print(knotname)

if __name__ == "__main__":
    main()
    