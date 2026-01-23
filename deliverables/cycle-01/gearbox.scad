// gearbox.scad (cycle-01)
// Minimal print-in-place gearbox (2-gear reduction) for FDM printers.
// Export: OpenSCAD -> F6 (Render) -> File -> Export -> Export as STL.
// Notes:
// - Uses simple rectangular gear teeth (not involute). Designed for reliability, not efficiency.
// - Print-in-place requires tuned clearances; start with clearance=0.45 for typical FDM.

$fn = 80;

// -------- Parameters --------
clearance = 0.45;        // gap between moving parts (mm)
wall      = 2.0;         // housing wall thickness (mm)
base_th   = 3.0;         // base thickness (mm)
height    = 12.0;        // gear thickness (mm)

// Gear pair (ratio ~= N2/N1)
N1 = 12;                 // pinion teeth
N2 = 24;                 // gear teeth
module_mm = 1.6;         // tooth pitch module-like value (mm) (tuned for chunky teeth)

// Derived sizes
pitch_r1 = (N1 * module_mm) / 2;
pitch_r2 = (N2 * module_mm) / 2;

// Tooth geometry (simple blocks)
tooth_w  = module_mm * 0.95;   // tangential width at pitch circle
radial_h = module_mm * 0.75;   // radial tooth height

// Shaft & bearing-ish clearances
shaft_r        = 3.0;
hub_r_extra    = 2.0;
axial_gap      = clearance;    // vertical gap above/below gears

// Center distance for meshing
center_dist = pitch_r1 + pitch_r2 + clearance;

// Housing interior margins
pad = 3.0;

// -------- Helpers --------
module ring(r_in, r_out, h){
    difference(){
        cylinder(r=r_out, h=h);
        translate([0,0,-0.1]) cylinder(r=r_in, h=h+0.2);
    }
}

module shaft_with_clearance(h){
    // the actual shaft solid
    cylinder(r=shaft_r, h=h);
}

module bore_for_shaft(h){
    // used for subtractive clearance around shaft
    cylinder(r=shaft_r + clearance, h=h);
}

module simple_spur_gear(N, pitch_r, gear_h){
    // Body
    union(){
        cylinder(r=pitch_r - radial_h*0.4, h=gear_h);
        // Teeth
        for(i=[0:N-1]){
            angle = 360*i/N;
            rotate([0,0,angle])
                translate([pitch_r, 0, 0])
                    cube([radial_h, tooth_w, gear_h], center=true);
        }
    }
}

module gear_on_shaft(N, pitch_r, gear_h, shaft_h){
    difference(){
        union(){
            // hub
            cylinder(r=shaft_r + hub_r_extra, h=gear_h);
            // gear
            simple_spur_gear(N, pitch_r, gear_h);
            // shaft
            translate([0,0,-(shaft_h-gear_h)]) shaft_with_clearance(shaft_h);
        }
        // through bore to create a print-in-place clearance between shaft and housing
        // (shaft is part of this gear; housing will have a larger hole)
    }
}

module housing(){
    // Compute interior bounds
    interior_x = center_dist + pitch_r1 + pitch_r2 + 2*pad;
    interior_y = max(pitch_r1, pitch_r2)*2 + 2*pad;
    interior_z = base_th + axial_gap + height + axial_gap + 3.0;

    outer_x = interior_x + 2*wall;
    outer_y = interior_y + 2*wall;
    outer_z = interior_z + wall;

    difference(){
        // Outer shell
        translate([-outer_x/2, -outer_y/2, 0])
            cube([outer_x, outer_y, outer_z]);

        // Inner cavity
        translate([-interior_x/2, -interior_y/2, base_th])
            cube([interior_x, interior_y, interior_z]);

        // Shaft holes (with clearance)
        translate([-center_dist/2, 0, 0]) bore_for_shaft(outer_z);
        translate([ center_dist/2, 0, 0]) bore_for_shaft(outer_z);

        // Top opening to ensure nothing is trapped by bridges (optional window)
        // Keep a rim for strength.
        rim = wall + 1.0;
        translate([-(outer_x-2*rim)/2, -(outer_y-2*rim)/2, outer_z - (wall+2.0)])
            cube([outer_x-2*rim, outer_y-2*rim, wall+3.0]);
    }
}

module knob(r=10, h=6){
    union(){
        cylinder(r=r, h=h);
        for(a=[0:60:300]){
            rotate([0,0,a]) translate([r*0.75,0,0]) cylinder(r=2.2, h=h);
        }
    }
}

module output_flat(r=8, h=5){
    // simple output handle/disc
    cylinder(r=r, h=h);
}

// -------- Assembly --------
module assembly(){
    // Place gears inside the housing with axial gaps
    z0 = base_th + axial_gap;

    // Gear 1 (input) at -center_dist/2
    translate([-center_dist/2, 0, z0]){
        // gear thickness = height
        gear_on_shaft(N1, pitch_r1, height, base_th + axial_gap + height + axial_gap + wall);
        // input knob on top of shaft
        translate([0,0,height + axial_gap + 1.0]) knob(r=11, h=6);
    }

    // Gear 2 (output) at +center_dist/2
    translate([ center_dist/2, 0, z0]){
        gear_on_shaft(N2, pitch_r2, height, base_th + axial_gap + height + axial_gap + wall);
        translate([0,0,height + axial_gap + 1.0]) output_flat(r=9, h=5);
    }

    // Housing last (so it visually encloses)
    housing();
}

assembly();
