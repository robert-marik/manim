rm -r UrcityIntegral/
manim --save_sections riemann.py UrcityIntegral
manedit --quick_present_export media/videos/riemann/1080p60/sections/UrcityIntegral.json  --project_name UrcityIntegral
bash fix_presentation.sh UrcityIntegral/
scp -r UrcityIntegral/ cornus.mendelu.cz:html/manim/ 
