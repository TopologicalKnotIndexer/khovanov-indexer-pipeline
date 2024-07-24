# khovanov-indexer-pipeline
基于 khovanov 同调的扭结类型识别管线，从分子数据文件到扭结名。

下载方式 `git clone git@github.com:TopologicalKnotIndexer/khovanov-indexer-pipeline.git --recursive`，注意一定要指明 `--recursive`，否则子模块不能正确下载。



## 前置条件

- `linux`, `x86_64`
- `python3`
- `openjdk`



## 使用方式

- `python3 ./src/main.py <FILEPATH>`
  - 程序会从 `<FILEPATH>` 处读入一个文本文件，并将其中存储的扭结信息转化为 `PD_CODE`
  - 最后再将 `PD_CODE` 依照 `khovanov` 同调推测起扭结名，若有多个扭结命中，则每行输出一个扭结名

