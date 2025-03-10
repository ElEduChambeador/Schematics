# An .SCR generator for export netlists or pngs based on a .sch file
- This files must be on the root folder of Eagle ("C:\EAGLE 9.6.2")
- All the schematics files must be inside a folder named RootCUBOs, there could be subfolders as long as they are inside RootCUBOs

How it works:
- Place all the .sch files or folders containing them inside 

> C:\EAGLE 9.6.2\RootCUBOs

- Place the .bat files inside 
> C:\EAGLE 9.6.2
1. Run the specified .bat file for the task (export pngs or netlists)
2. It will generate a .scr file with the same name of the .bat file
3. Open Eagle
4. Select File -> New -> Schematic
5. Click on 'Execute Script' (the blue 'SCR' icon)
6. Select browse and go to the "C:\EAGLE 9.6.2" folder and select the desired .scr file
7. Press and hold 'enter' to every promt window that appears
8. Wait until no more schematics are opened
9. Repeat the process from point '2.' every time a new batch of schematics is placed inside the folder RootCubos 

#### Disclaimer
- The warning message of no backward annotations appears due to de fact that there are not .brd file linked to the .sch file, this warning can be overlooked.
- If an error about an incorrect path appears, restart Eagle (haven't found a way to fix it, so restart is the only option)