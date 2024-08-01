- [新特性](#new-feature)
- [关服](#shut-down-server)
- [开服](#sweety-home)
- [OverView](#overview)
- [How To Build It](#how-to-build-it)
  - [python version](#python-version)
    - [Build From Source](#build-from-source)
    - [Download Binary](#download-binary)
  - [c++ version](#c-version)
- [How To Use It](#how-to-use-it)
- [Core Config](#core-config)
- [TODO List](#todo-list)
- [Report Bug And Advice](#report-bug-and-advice)
- [Relate Tools And Repo](#relate-tools-and-repo)
- [Useful WebSite](#useful-website)

# New Feature
Different environment or different monitor color need different HSV color range.

Debuging the image to get correct HSV is needed ASAP.

对于不同环境或者不同显示器颜色，获取鱼漂颜色范围有差异，自己在使用的时候会遇到这种问题。

所以需要添加调试颜色范围的功能。

# Shut Down Server
一晃眼关服已经差不多七个月了，写的脚本也没了用武之地，每个大版本的初期都是赚钱的好时候。

10.0初期，脚本也给我带来了300多万的收益。10.0也把心心念的麦卡也完工了。

想念我的麦卡完工，想念我的奶骑，想念跟朋友一起冲层的时光。
希望国服快快回归吧，虽然不太现实。
想拿一条水獭给18年的青春画上一个句号。

# Sweety home
2024-04-10，微软网易又再次重新合作了，看来水獭又有机会拿到了

# OverView
Auto Fising Script with GUI.
Rate of success catching fishing is over **90%**.

# How To Build It
## python version
### Build From Source
1. Download ```python3``` from **MicroSoft Store**, version(3.10)
2. Download ```vs code``` from **MicroSoft Store** [Optional]
3. Get This Repo via [Git](https://gitforwindows.org/) or [Zip](https://github.com/Greetlist/wow_fishing_script/archive/refs/heads/master.zip) and cd into ```python_version``` dir
4. Download Python packages ```pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple```
5. Run build bat: ```./build.bat```
6. binary is ```dist/main/main.exe```

### Download Binary
[Release Page](https://github.com/Greetlist/wow_fishing_script/releases)
## c++ version
TODO

# How To Use It
[ForeGround Example GIF](https://1drv.ms/u/s!ArufjyMgeESVgc9x5MZkED7NZo_KGQ?e=cW1eAh)

[BackGround Example GIF](https://1drv.ms/u/s!ArufjyMgeESVgc9zOjW1tHBFcisxEA?e=Zh2iTy)

> Notice: BackGround Mode need 3 prepare works before fishing
1. Turn Interact On

![Turn On](https://img.ppcn.net/uploadfile/2022/1028/20221028153852683.png)

2. execute these two macro

```
/console SoftTargetInteractArc 2      # allowed you to interact without facing things
/console SoftTargetInteractRange 50   # increase your interact range to 50
```

3. Bind interact key to **'9'**

![Interact Key Setting](https://olimg.3dmgame.com/uploads/images/raiders/2022/0830/1661822926765.png)

# Core Config
1. Fishing area. (Coordinate of screen is auto-complete, support multi-screen, **not support cross-screen**)
2. Game Window Name. (Adjust different language)
3. Fishing Idle Time.
4. Cast Some Skill Periodically [keyboard '6']. (toy or bait)
5. Switch To TestMode. (Take some screenshot for testing)
6. Switch To FG/BG Mode. (BG Mode allow you to do something else while WOW window is inactive)
7. Use Coordinate judgement or Area Judgement. (Coordinate Judgement is more stable while testing in real game)
8. Max Fishing Count, :warning: **0 is not infinity, Please Increase this value manually**
9. Probability Of Jumping before every fishing (default: 10%).

# TODO List
- [x] Add Max-Fishing-Count config.
- [x] Add Random Jump and Jump probability config.
- [ ] Support invoke some WOW's Macro before fishing.
- [ ] Auto Online/Offline.
- [ ] Key Binding configurable.
- [ ] Auto change coordinate threshold. (Reinforcement)
- [ ] Auto change Fish-Float hsv color range to fit different environment. (Reinforcement)

# Report Bug And Advice
If you trapped with some unknown bugs or want to give some advice, Please [new issue](https://github.com/Greetlist/wow_fishing_script/issues/new/choose) to me.

# Relate Tools And Repo
[PySide6](https://doc.qt.io/qtforpython/#)

[pywin32](https://github.com/mhammond/pywin32)

[pyautogui](https://github.com/asweigart/pyautogui)

[pyinstaller](https://github.com/pyinstaller/pyinstaller)

[python-mss](https://github.com/BoboTiG/python-mss)

[opencv-python](https://github.com/opencv/opencv-python)

# Useful WebSite
[MicroSoft Win32 API](https://learn.microsoft.com/en-us/windows/win32/)

[PySide6 Tutorials](https://www.pythonguis.com/tutorials/)

[pywin32 Online API](http://timgolden.me.uk/pywin32-docs/)

[How-To-Send-Key-To-Inactive-Window](https://stackoverflow.com/questions/12996985/send-some-keys-to-inactive-window-with-python)

[MicroSoft Win32 Virtual Key Binding](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)

[HSV Color Range Switcher](https://stackoverflow.com/a/59906154/13747065)
