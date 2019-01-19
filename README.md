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
## Characteristics
### Multi-thread
本專案中大量使用multi-thread的技巧，來避免不相干的任務互相干擾(如影片回傳與超音波偵測、甚至是雷射光攻擊)
### Strict hierarchy
本專案使用arduino開發板來處理大量重複性高的簡單任務，例如馬達的操控，以及超音波訊號接收等等。在arduino上做的簡單初步處理，既可以分擔RPi
的運算壓力，也解決了RPi的digital pin不足的情況(Rpi的digital pin共有17個，但本專案會用到超過60個digital i/o pin腳。
### Various transmission skills
本專案根據不同的傳輸資料類型，來選擇最適合的傳輸方式。遙控訊號部份我們選擇使用藍芽，避免網路不佳時無法進行簡單的遙控功能。大流量的影片回
傳，則使用效率最高的網路傳輸。Rpi跟arduino之間的聯絡方式也包刮了serial connection、GPIO訊號，由於車身的旋轉功能，使得
大部份部份的serial線路無法使用，因此我們使用了後兩者來客服本問題。在處理大量的數位訊號時，為了避免Rpi的GPIO pin腳不夠，我們甚至採取了將
數位信號類比化的技巧，並且以單一一個pin腳的PWM信號來傳送。
## Implementation
本專案由遠端的遙控中心加上遙控探測車組成。車上裝置又可以分為4個部分：車體、超音波攻擊方位辨識裝置、影像辨識系統、反擊裝置。在裝置行進間，
會隨時以超音波接收裝置偵測有沒有受到攻擊源的攻擊(以超音波發射來模擬)，若收到攻擊，車體會停止前進，進入偵測辨識模式。在此模式中，車子會先
以超音波接收器大概得知攻擊方位，接者使用影像辨識來精確判斷，並同時用步進馬達控制砲台及相機對準攻擊源。下圖為我們使用的攻擊源圖示，以及影
像辨識系統實際瞄準的情形。  
![target](https://user-images.githubusercontent.com/31982568/51428977-b74ad780-1c44-11e9-9fdc-b68f52c6fbbf.png)
![recognition](https://user-images.githubusercontent.com/31982568/51429061-ce3df980-1c45-11e9-8fca-7f4a464fda67.jpg)
以下為各部分的實作解說。
### Remote control signal
使用藍芽進行傳輸，在local端以電腦連接裝載HC-05藍芽模組的arduino，並且上傳以下程式。
```
local/arduino/remote_control/remote_control.ino
```
電腦會接收鍵盤的上下左右指令，並且傳送到RPi端，回傳RPi的state(control/attacked & detection/recognition/attacking其中之一)給電腦控制
者，RPi方面相對應的則為以下程式。
```
remote/A_CAR/remote_control.py
```
### Video stream
透過網路使用TCP protocol在local end(client)與RPi(server)之間傳遞。在每一輪的開始，由client端首先發出"ready"訊號，接著接收RPi camera攝
得的影像檔案。由於單一一個影像的檔案也過於巨大，超過python TCP socket可靠傳送的上限，因此我們會將一個frame分為數個檔案傳送，至本機端才重新
組合成完整的影像。以上流程不斷重複，就可以得到完整的及時的影片。  
為了怕影片傳送速度過慢，拖慢了其他任務(如基本的遙控指令)的效率，因此我們在此使用multi thread的技巧來實作。
這部份的程式，主要寫在以下兩個檔案中。
```
local/GUI/video_serial_client.py
remote/A_CAR/video_serial_server.py
```
### GUI
我們實作了一個簡單的GUI於以下檔案中，會顯示使用者操縱介面以及遙控車回傳的即時影片，並且在受到攻擊時會顯示於螢幕上，藉以警告操縱者(當然，由遠
端RPi自動進行反擊)。
```
local/GUI/command_center.py
```
下圖為GUI顯示的範例畫面。
![GUI](https://user-images.githubusercontent.com/31982568/51429810-9dfa5900-1c4d-11e9-836f-2d82ab4ce39c.png)
### Power chain
車體使用六輪越野車，Rpi以藍芽接收到控制訊號後，受限於pin腳數量以及旋轉扭線的問題，只得選擇使用GPIO傳送PWM訊號給arduino做為控制訊號。我們將前
後左右四個boolean value經過簡單的encoding轉為單一一個類比訊號，並將PWM切為16等分，傳到arduino端後再解開還原成原本的訊號，解此達成許多複雜的
動作，包括前進、後退、左、右、左前、右前、左後、右後、原地旋轉、全速前進、慢速前進等等。
```
remote/arduino/wheel_controller/wheel_controller.ino
remote/A_CAR/PWM_io.py
```
### Attacking detection
以超音波發送接收模組hcsr-04做為模擬攻擊/接收源，每個超音波元件接收的角度大約為60度的扇形區域，經過測試之後，我們將整個圓切為八等分，每個等分上
有兩個仰角不同(0度以及45度)的超音波發射接收器，再加上天頂的最後一個，車身上一共有17個超音波接收器。由於接收器數量過多，因此總共需要兩個arduino
才能提供足夠的腳位，兩者分別接收超音波接收器的訊號，並經由serial port傳送一個17bit的訊號給rpi，程式實現如下：
```
remote/arduino/sensor_1/sensor_1.ino
remote/arduino/sensor_2/sensor_2.ino
```
### Target recognition
由於我們做的並不是一個普遍的辨識功能，而是有特殊的目標，且在我們的設定中，辨識系統的效率必須非常高，才能在RPi達成即時的辨識，若有稍微嚴重的延遲
，步進馬達很有可能會轉過頭，或是來回找不到目標精準的位置，因此我們決定自主設計出一套辨識系統，可讓延遲控制在0.1秒以內，比坊間的臉部辨識等等動輒
3~5秒的延遲有效率許多。
#### Searching
在辨識的第一階段中，我們從convolutional neural network得到靈感，精心設計了許多不同大小的filter，滑過一個影片的frame，並且根據結果回傳匹配值
。針對不同的filter大小，我們對於圖片的down sampling以及匹配值的臨界值都有精心的設計，且這些設計皆可以隨著辨識環境來調整。當然，我們也在事先對
影像做了標準化，因此大幅提升辨識系統的除錯能力，甚至在半夜視環境(白天關燈的實驗室)中，也能正確無誤的辨識。
#### Tracing
經過第一階段找出可能的候選清單後，遙控車的炮台就會開始轉動，而架在砲口旁的相機也會隨之轉動。轉動造成的干擾恰好可以對辨識的品質進行篩選，在searching
階段中的fake truth，經過些微的擾動以後，會與真正的目標產生明顯差距，因此經過幾個循環之後，候選清單中就只剩下真正的目標。接著我們的辨識系統會把
目標鎖定在該影像周邊的一小塊區域中，更進一步提升辨識的效率，以換取更多的辨識次數，來即時調整辨識參數，避免由於砲台轉動造成的影像變化，使得辨識的
效果下降。
### Counter system
砲台上同時裝備了Pi camera以及雷射模組，因此在tracing過程中，系統會以將目標移動到螢幕正中央為目標，不斷調整砲台的方位以及仰角，最後開火，擊潰
外星人！
## Deployment
首先完成線路的連接，並且將負責local藍芽傳輸、車輪控制以及超音波偵測的arduino開發版寫入相對應的程式，接著在RPi上值型以下指令：
```
cd remote/A_CAR
bash CARS.sh
```
遙控車即會開機，並且開始超音波攻擊源偵測以及錄影功能，以及與本機端的藍芽模組進行連接。  
接著在本機輸入以下指令：
```
cd local/GUI
python3 command_center.py
```
本機端會開啟影像串流，並且開始傳送遙控信號，進行外星探險活動！
## Achievements
## Reference
## Authors
## License
