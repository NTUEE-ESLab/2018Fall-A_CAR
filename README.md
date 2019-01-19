# 2018Fall_A-CAR(Automatic Counter-Attack Rover)

## Materials
Raspberry Pi 3  
Rpi camera
Arduino * 4  
L298N motor driver * 3  
JGA25-370 motor * 6  
5V stepper motor with ULN2003 stepper motor driver * 2  
hcsr-04 ultrasonic module  
toy car  
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
## Implementation
本專案由遠端的遙控中心加上遙控探測遮組成。車上裝置又可以分為4個部分：車體、超音波攻擊方位辨識裝置、影像辨識系統、反擊裝置。在裝置行進間，
會隨時以超音波接收裝置偵測有沒有受到攻擊源的攻擊(以超音波發射來模擬)，若收到攻擊，車體會停止前進，進入偵測辨識模式。在此模式中，車子會先
以超音波接收器大概得知攻擊方位，接者使用影像辨識來精確判斷，並同時用步進馬達控制砲台及相機對準攻擊源。下圖為我們使用的攻擊源圖示，以及影
像辨識系統實際瞄準的情形。  
以下為各部分的實作解說。
車體：六輪越野車，馬達選用JGA25-370，driver選用L298N，rpi接收電腦傳出的藍芽訊號，以GPIO傳送PWM訊號給arduino做為控制訊號，將PWM切為16等分，每個等分代表一個動作(前進、後退、左、右、左前、右前、左後、右後、原地旋轉、全速前進、慢速前進等)。
 
攻擊方位辨識裝置：
以超音波發送接收系統hcsr 04做為模擬攻擊接收源，一個超音波接收角度大約左右30度總共60度，所以一個平面需要3個不同角度的接收器來接收不同角度的攻擊，在經過測試之後，我們將整個圓切為八等分，每個等分上有兩個個接收不同角度的超音波發射接收器，就可以準確的辨識出攻擊方向，所以總計使用了17個超音波接收發送器，一個放在車頂來偵測上方來的攻擊。超音波接收器接收到訊號之後會經由Arduino Serial port傳送一個8bit的訊號給rpi，rpi再控制反擊裝置轉向接收到的方位，右圖為超音波發送接收器示意圖，如果2號的接收器收到訊號，arduino會傳送01000000的訊號給rpi。
影像辨識系統：
(你的)
反擊裝置：與影像辨識系統的pi camera裝在一起，影像辨識系統確認攻擊源後由rpi啟動雷射模組進行攻擊

## Deployment
## Achievements
## Reference
## Authors
## License
