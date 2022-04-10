rm -r AS_vlastni_cisla
manim --save_sections AS_vlastni_cisla.py Nadpis
manim --save_sections AS_vlastni_cisla.py Ukazky
manim --save_sections AS_vlastni_cisla.py Description
manim --save_sections AS_vlastni_cisla.py PhasePortrait
manedit --quick_present_export media/videos/AS_vlastni_cisla/1080p60/sections/Nadpis.json --quick_present_export media/videos/AS_vlastni_cisla/1080p60/sections/Ukazky.json --quick_present_export media/videos/AS_vlastni_cisla/1080p60/sections/Description.json --quick_present_export media/videos/AS_vlastni_cisla/1080p60/sections/PhasePortrait.json --project_name AS_vlastni_cisla 
bash fix_presentation.sh AS_vlastni_cisla 
scp -r AS_vlastni_cisla cornus.mendelu.cz:html/manim/ 
