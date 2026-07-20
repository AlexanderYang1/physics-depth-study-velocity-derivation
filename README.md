# Physics Depth Study: Downwards Velocity Derivation and Comparison of Vertical Acceleration
Intergration is utilized to find velocity after rotating acceleration vectors to align with real-world acceleration.  
The downwards vertical velocity will be taken as the phone's down direction is always known, while horizontal direction
is relative to the device's starting rotation.


From derived velocity, motion during the descent can be identified and compared. The method utilized to derive a clean
acceleration sample, is the taking of the mid-section of the velocity graph where the object is descending the slope,
and calculating the gradient, deriving acceleration.

## Structure
`data/` contains the raw sensor data of all of the trials for Object A and Object B.  
`out/` contains generated graphs.  
`src/` contains the code utilized to produce derived data.

## References
Matplotlib. (2012). *Matplotlib: Python plotting — Matplotlib 3.1.1 documentation.*
https://matplotlib.org

Scipy.Org. (2024). *Rotation — SciPy v1.14.0 Manual. (2024)*. 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html

Robotics Stack Exchange. (2019) *How to transform raw accelerometer data into the Earth fixed frame to determine position.*
https://robotics.stackexchange.com/questions/18446/how-to-transform-raw-accelerometer-data-into-the-earth-fixed-frame-to-determine 



