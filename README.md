# bds-Sim
北斗信号模拟。

BeiDou navigation satellite system signal simulator.

# 项目目标

我们希望能够实现一个完整的北斗卫星定位信号软件无线电模拟源。

# 本分支

目前我们已经基本完成了B1I、B1C导航电文的生成、伪距以及其修正的处理。然而，在利用SDR产生实际发射信号的代码逻辑依旧存在问题。

在旧的项目中，我们将两部分代码合并在了一个仓库中，这既带来了配置上的麻烦，也使得整个项目变得混乱。

因此我考虑将实际信号调制部分分离出去，建立一个新的分支，而这个分支仅仅包含了Python实现的导航电文和伪距生成部分。

# 运行方法

本项目需求应该是Python 3.10及以上，需求的第三方模块在`requirements.txt`中。

运行`generate_beidou_info.py`可以生成导航电文和伪距信息：

```bash
python .\generate_beidou_info.py -p 120 30 0 -a .\bdsTx\satellite_info\almanac\tarc0190.23alc.json -e .\bdsTx\satellite_info\ephemeris\tarc0140.json -s B1I -i .\bdsTx\satellite_info\ionosphere\iono_corr.json -r .\bdsTx\coding\ranging_code\ -b 300 -o output.json
```

具体参数说明请查看`generate_beidou_info.py --help`的输出提示。