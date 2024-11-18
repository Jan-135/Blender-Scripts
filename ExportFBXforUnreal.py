bl_info = {
    "name": "Export to FBX for Unreal Engine",
    "author": "Jan Ferber",
    "version": (1, 1),
    "blender": (4, 2, 2),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "category": "Export Animation",
}


import bpy
import os

# Liste der Charaktere für das Dropdown-Menü
character_options = [
    ("Maurice", "Maurice", ""),
    ("Mother_Golem", "Golem Mutter", ""),
    ("Bird", "Vöglein vöglein", ""),
    ("Testosteron", "Testosteron", ""),
]

# Liste der Szenen für das Dropdown-Menü
scene_options = [
    ("Szene002", "scene002", ""),
    ("Szene003", "scene003", ""),
    ("Szene004", "scene004", ""),
    ("Szene005", "scene005", ""),
    ("Szene006", "scene006", ""),
    ("Szene007", "scene007", ""),
    ("Szene008", "scene008", ""),
    ("Szene009", "scene009", ""),
    ("Szene010", "scene010", ""),
    ("Szene011", "scene011", ""),
    ("Szene012", "scene012", ""),
    ("Szene013", "scene013", ""),
    ("Szene014", "scene014", ""),
    ("Szene015", "scene015", ""),
    ("Szene016", "scene016", ""),
    ("Szene017", "scene017", ""),
    ("Szene018", "scene018", ""),
    ("Szene019", "scene019", ""),
    ("Testosteron", "testosteron", ""),
]

# Property für die Charakterauswahl
bpy.types.Scene.character_selector = bpy.props.EnumProperty(
    name="Select Character",
    description="Choose the character for the animation export",
    items=character_options,
)

# Property für die Szenenauswahl
bpy.types.Scene.scene_selector = bpy.props.EnumProperty(
    name="Select Scene",
    description="Choose the scene for the animation export",
    items=scene_options,
)

# Funktion zur Berechnung der nächsten Version
def get_next_version(export_path, character, scene):
    # Zählt die Anzahl der Dateien im Zielordner, die mit dem Charakter und der Szene beginnen
    existing_files = [f for f in os.listdir(export_path) if f.startswith(f"{character}_{scene}_v")]
    version_numbers = []

    # Extrahiere die Versionsnummern aus den Dateinamen
    for file in existing_files:
        parts = file.split('_')
        if len(parts) > 2 and parts[2].startswith('v'):
            try:
                version_numbers.append(int(parts[2][1:]))  # Nummer nach 'v' extrahieren
            except ValueError:
                continue

    # Falls keine Versionen gefunden wurden, starte mit Version 1
    if not version_numbers:
        return 1

    # Die nächste Version ist die größte existierende Version + 1
    return max(version_numbers) + 1

# Operator zum Exportieren nach FBX mit spezifischen Einstellungen
class ExportToFBXOperator(bpy.types.Operator):
    bl_idname = "export_scene.fbx_unreal"
    bl_label = "Export to FBX for Unreal"

    def execute(self, context):
        # Charakter und Szene aus der Dropdown-Auswahl abfragen
        selected_character = context.scene.character_selector
        selected_scene = context.scene.scene_selector

        # Basis-Exportpfad
        base_path = "N:/GOLEMS_FATE/animations"
        # Charakter- und Szenen-Unterordner erstellen
        export_path = os.path.join(base_path, selected_character, selected_scene)
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # Berechne die nächste Version
        version = get_next_version(export_path, selected_character, selected_scene)

        # Vollständiger Exportpfad inklusive Dateiname mit Versionierung
        export_file_name = f"{selected_character}_{selected_scene}_v{version}.fbx"
        export_file_path = os.path.join(export_path, export_file_name)

        # Überprüfen, ob die Datei bereits existiert
        while os.path.exists(export_file_path):
            version += 1  # Version um 1 erhöhen
            export_file_name = f"{selected_character}_{selected_scene}_v{version}.fbx"
            export_file_path = os.path.join(export_path, export_file_name)

        # Export-Einstellungen für Unreal Engine
        bpy.ops.export_scene.fbx(
            filepath=export_file_path,           # Exportpfad
            use_selection=True,                  # Nur ausgewählte Objekte exportieren
            apply_scale_options='FBX_SCALE_NONE', # Skalierungsoption
            bake_anim=True,                      # Animationen backen
            bake_anim_use_all_bones=True,        # Alle Bones in der Animation verwenden
            bake_anim_use_nla_strips=False,      # NLA-Strips ignorieren
            bake_anim_use_all_actions=False,     # Alle Actions backen
            bake_anim_force_startend_keying=True,# Keyframes am Anfang und Ende setzen
            object_types={'ARMATURE'},           # Nur Armatures exportieren
            mesh_smooth_type='OFF',              # Smoothing-Option
            use_armature_deform_only=False,      # Nur deformierende Bones exportieren
            add_leaf_bones=False,                # Leaf-Bones weglassen
            axis_forward='X',                    # Achsen-Konfiguration
            axis_up='Z',                          # Achsen-Konfiguration
            global_scale=1.0                     # Setze den globalen Skalierungsfaktor auf 1.0
        )
        
        self.report({'INFO'}, f"Export nach FBX für {selected_character} in {selected_scene} erfolgreich!")
        return {'FINISHED'}

# Benutzeroberfläche des Add-ons
class ExportFBXPanel(bpy.types.Panel):
    bl_label = "Export to FBX for Unreal"
    bl_idname = "PT_ExportFBXPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Export to FBX'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Sei glücklich mit dem was du hast.", icon='FUND')
        
        # Label für die Charakter-Auswahl
        layout.prop(context.scene, "character_selector", text="Character")  # Dropdown für Charakterauswahl

        # Label für die Szenen-Auswahl
        layout.prop(context.scene, "scene_selector", text="Szene:")      # Dropdown für Szenenauswahl
        
        # Label für den Export-Button
        row = layout.row()
        row.operator("export_scene.fbx_unreal", text="Exportiere Animation als FBX für Unreal")  # Export-Button


# Registrierung des Panels und Operators
def register():
    bpy.utils.register_class(ExportToFBXOperator)
    bpy.utils.register_class(ExportFBXPanel)
    bpy.types.Scene.character_selector = bpy.props.EnumProperty(items=character_options)
    bpy.types.Scene.scene_selector = bpy.props.EnumProperty(items=scene_options)

def unregister():
    bpy.utils.unregister_class(ExportToFBXOperator)
    bpy.utils.unregister_class(ExportFBXPanel)
    del bpy.types.Scene.character_selector
    del bpy.types.Scene.scene_selector

if __name__ == "__main__":
    register()
