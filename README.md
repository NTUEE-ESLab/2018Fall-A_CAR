# 2018Fall_A-CAR(Automatic Counter-Attack Rover)

## Materials
Raspberry Pi 3 * 1  
Rpi camera * 1
Arduino * 4  
L298N motor driver * 3  
JGA25-370 motor * 6  
5V stepper motor with ULN2003 stepper motor driver * 2  
HC-05 bluetooth module * 1
hcsr-04 ultrasonic module * 20  
toy car * 1  
local-end computer(windows device)  
any electronic and mechanical materials needed  
## Prerequisites
### Raspberry pi
OpenCV 3.0 +  
Rpi.GPIO 0.6.5  
pySerial 3.0 +  
numpy 1.14.0  
scipy 1.0.0  
socket 1.0.0  
### Windows local-end
pygame 1.9.4  
numpy 1.14.0  
socket 1.0.0  
pySerial 3.4  
scipy 1.0.0  
pypiwi32-222  
### Arduino
NewPing(already in the folder)  
## Motivation
在可預見的未來，外星探測任務將會大量進行。倘若探測車出任務時，遇到不明物體攻擊，必需及時反擊，但是從地球傳出的訊號到達宇宙某處的探測車，
需要相當的時間，不可能由人為操作反擊。所以我們開發出了一台搭載自動反擊系統的遙控車模型，可以在不需訊號傳遞的情況下，自動分辨攻擊的來向並
由攝影鏡頭辨識攻擊源加以反擊。  
我們以Raspberry Pi作為遙控車主機，在車體上加裝辨識裝置與反擊裝置，以藍芽模擬地球傳出的訊號來控制，超音波訊號模擬攻擊源的攻擊訊號，Pi
camera作為鏡頭，特定圖像來代表攻擊源，並自行開發出辨識演算法，最後以紅光雷射作為車上的反擊裝置。
## characteristic
### multi-thread
本專案中大量使用multi-thread的技巧，來避免不相干的任務互相干擾(如影片回傳與超音波偵測、甚至是雷射光攻擊)
### Strict hierarchy
本專案使用arduino開發板來處理大量重複性高的簡單任務，例如馬達的操控，以及超音波訊號接收等等。在arduino上做的簡單初步處理，既可以分擔RPi
的運算壓力，也解決了RPi的digital pin不足的情況(Rpi的digital pin共有17個，但本專案會用到超過60個digital i/o pin腳。
### Various transmission
本專案根據不同的傳輸資料類型，來選擇最適合的傳輸方式。遙控訊號部份我們選擇使用藍芽，避免網路不佳時無法進行簡單的遙控功能。大流量的影片回
傳，則使用效率最高的網路傳輸。Rpi跟arduino之間的聯絡方式也包刮了serial connection、GPIO訊號，由於車身的旋轉功能，使得
大部份部份的serial線路無法使用，因此我們使用了後兩者來客服本問題。在處理大量的數位訊號時，為了避免Rpi的GPIO pin腳不夠，我們甚至採取了將
數位信號類比化的技巧，並且以單一一個pin腳的PWM信號來傳送。
## Implementation and Deployment
本專案由遠端的遙控中心加上遙控探測車組成。車上裝置又可以分為4個部分：車體、超音波攻擊方位辨識裝置、影像辨識系統、反擊裝置。在裝置行進間，
會隨時以超音波接收裝置偵測有沒有受到攻擊源的攻擊(以超音波發射來模擬)，若收到攻擊，車體會停止前進，進入偵測辨識模式。在此模式中，車子會先
以超音波接收器大概得知攻擊方位，接者使用影像辨識來精確判斷，並同時用步進馬達控制砲台及相機對準攻擊源。下圖為我們使用的攻擊源圖示，以及影
像辨識系統實際瞄準的情形。  
![target](https://user-images.githubusercontent.com/31982568/51428977-b74ad780-1c44-11e9-9fdc-b68f52c6fbbf.png)
![recognition](https://user-images.githubusercontent.com/31982568/51429061-ce3df980-1c45-11e9-8fca-7f4a464fda67.jpg)
以下為各部分的實作解說。
### remote control signal
使用藍芽進行傳輸，在local端以電腦連接裝載HC-05藍芽模組的arduino，並且上傳以下程式。
```
local/arduino/remote_control/remote_control.ino
```
電腦會接收鍵盤的上下左右指令，並且傳送到RPi端，回傳RPi的state(control/attacked & detection/recognition/attacking其中之一)給電腦控制
者。
### Video stream
透過網路使用TCP protocol在local end(client)與RPi(server)之間傳遞。在每一輪的開始，由client端首先發出"ready"訊號，接著接收RPi camera攝
得的影像檔案。由於單一一個影像的檔案也過於巨大，超過python TCP socket可靠傳送的上限，因此我們會將一個frame分為數個檔案傳送，至本機端才重新
組合成完整的影像。以上流程不斷重複，就可以得到完整的及時的影片。  
為了怕影片傳送速度過慢，拖慢了其他任務(如基本的遙控指令)的效率，因此我們在此使用multi thread的技巧來實作。

車體：六輪越野車，馬達選用JGA25-370，driver選用L298N，rpi接收電腦傳出的藍芽訊號，以GPIO傳送PWM訊號給arduino做為控制訊號，將PWM切為16等分，每個等分代表一個動作(前進、後退、左、右、左前、右前、左後、右後、原地旋轉、全速前進、慢速前進等)。
 
攻擊方位辨識裝置：
以超音波發送接收系統hcsr 04做為模擬攻擊接收源，一個超音波接收角度大約左右30度總共60度，所以一個平面需要3個不同角度的接收器來接收不同角度的攻擊，在經過測試之後，我們將整個圓切為八等分，每個等分上有兩個個接收不同角度的超音波發射接收器，就可以準確的辨識出攻擊方向，所以總計使用了17個超音波接收發送器，一個放在車頂來偵測上方來的攻擊。超音波接收器接收到訊號之後會經由Arduino Serial port傳送一個8bit的訊號給rpi，rpi再控制反擊裝置轉向接收到的方位，右圖為超音波發送接收器示意圖，如果2號的接收器收到訊號，arduino會傳送01000000的訊號給rpi。
影像辨識系統：
(你的)
反擊裝置：與影像辨識系統的pi camera裝在一起，影像辨識系統確認攻擊源後由rpi啟動雷射模組進行攻擊

## Achievements
## Reference
## Authors
## License
