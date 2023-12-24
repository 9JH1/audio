# audio visuliser 
this is a audio visuliser I made for windows ten, it displays the title of the currently playins song on spodify and shows a bar displaying the sound 
```
Mitski - My Love Mine All Mine | [||||||||||||||||||||||||||||                      ]
```
it changes the title and the bar every 0.01 second, if it does not work and shows this error 
```
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2032.0_x64__qbz5n2kfra8p0\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2032.0_x64__qbz5n2kfra8p0\Lib\multiprocessing\process.py", line 108, in run       
    self._target(*self._args, **self._kwargs)
  File "e:\Projects\[ collection ] python projects\audio.py", line 109, in update
    print(f"\r{format_title(windowDict['Spotify.exe'])} | {generate_percentage_bar(percentage)}",end='', flush=True)
                            ~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: 'Spotify.exe'
```
then open spodify as a window instead of minimsied. this program will not work unless you are on windows
