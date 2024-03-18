# 工具

> IMMORTAL OMNISSIAH, HEAR OUR PRAYS!

这里包含了部分工具的使用说明以及测试方式说明。

## 星历文件预处理

项目中的模块`bdsTx.satellite_info`中包含了一部分星历文件的处理数据，用于从CSNO的广播数据生成我们程序使用的json星历文件。

请查阅模块目录下`convert_ephemeris_to_json.py`和`convert_almanac_to_json.py`的输出信息以获取使用说明。

## 卫星测距码生成

项目中的模块`coding`包含了各类编码算法的实现，也包括了卫星测距码的生成算法。

因为每个卫星的测距码本身就是固定的，我们完全没必要每次运行程序的时候都重新生成一遍，因此`coding/ranging_code`下面已经包含了所有卫星的测距码。

当然，你可以重新生成和测试本项目生成卫星测距码的部分，你可以调用`coding`目录下的`xxx_ranging_code.py`来进行验证。

## 本地接收模拟

我们的接收测试采用[GNSS-SDR](https://github.com/gnss-sdr/gnss-sdr/)进行。对于GNSS-SDR的安装和基本的使用，请参考其[官方文档](https://gnss-sdr.org/docs/)的说明。

我们提供了简单的GNSS-SDR配置文件，用于北斗B1I信号的模拟接收测试，配置文件位于`tools/gnss-sdr-configs/`。