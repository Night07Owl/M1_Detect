# Camera Specification

**Sensor Name:** Integrated Camera (Manufacturer: Sonix)  
**Device PnP ID:** `USB\VID_3277&PID_0010&MI_00\7&DF5034D&0&0000`  
**Driver Model:** Windows USB Video Class (UVC)  
**OpenCV Backend:** DirectShow (`cv2.CAP_DSHOW`)  
**Tested Resolution:** 1280 x 720 (16:9 HD)  
**Default Resolution:** 640 x 480 (4:3 Standard)  
**Pixel Encoding / FourCC:** `YUY2`  
**Measured Empirical FPS:** 19.84 FPS  
**Average Frame Latency:** 50.39 ms  
**Latency 95th Percentile:** 63.81 ms  
**Disconnection Handling:** Graceful exception recovery on invalid index (`cap.isOpened() == False`)

