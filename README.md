- [How To Build It](#how-to-build-it)
  - [python version](#python-version)
    - [Build From Source](#build-from-source)
    - [Download Binary](#download-binary)
  - [c++ version](#c-version)
- [How To Run It](#how-to-run-it)
  - [UI](#ui)
- [Core Config](#core-config)
- [TODO List](#todo-list)
- [Relate Tools And Repo](#relate-tools-and-repo)
- [Useful WebSite](#useful-website)

# How To Build It
## python version
### Build From Source
1. Download ```python3``` from **MicroSoft Store**, version(3.10)
2. Download ```vs code``` from **MicroSoft Store** [Optional]
3. Get This Repo via [Git](https://gitforwindows.org/) or [Zip](https://github.com/Greetlist/wow_fishing_script/archive/refs/heads/master.zip) and cd into ```python_version``` dir
4. Download Python packages ```pip install -r requirement.txt```
5. Run build bat: ```./build.bat```
6. binary is ```dist/main/main.exe```

### Download Binary
[Release Page](https://github.com/Greetlist/wow_fishing_script/releases)
## c++ version
TODO

# How To Use It
## UI
[ForeGround Example](https://1drv.ms/u/s!ArufjyMgeESVgc9xulOQ0l8vUSvggg?e=roihca)
[BackGround Example](https://1drv.ms/u/s!ArufjyMgeESVgc9zWQXLlBx0YSuEzw?e=IJJqge)

> Notice: BackGround need execute these two macro before fishing and Bind interact key to '9'

```
/console SoftTargetInteractArc 2      # allowed you to interact without facing things
/console SoftTargetInteractRange 50   # increase your interact range to 50
```

![Interact Key Setting](https://1drv.ms/u/s!ArufjyMgeESVgc9yWnS1WWvchxQhKA?e=DOOu0h)

# Core Config
1. Fishing area. (Coordinate of screen is auto-complte, support multi-screen, **not support cross-screen**)
2. Game Window Name. (Adjust different language)
3. Fishing Idle Time.
4. Cast Some Skill Periodically. (Jump)
5. Switch To TestMode. (Take Some Screenshot)
6. Switch To FG/BG Mode. (BG Mode allow you to do something else while WOW window is inactive)
7. Use Coordinate judgement or Area Judgement. (Coordinate Judgement is more stable while testing in real game)

# TODO List
- [ ] Support invoke some WOW's Macro before fishing.
- [ ] Add fishing count config.
- [ ] Auto Online/Offline.
- [ ] Key Binding Configurable.
- [ ] Auto change coordinate threshold. (Reinforcement)

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