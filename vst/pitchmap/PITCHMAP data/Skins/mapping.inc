<?xml version="1.0" encoding="utf-8" ?>
<DUMMY>
    <!-- parameters definition -->
    <VARIABLE id="BYPASS" value="dsp.input0"/>
    <VARIABLE id="THRESHOLD" value="dsp.input1"/>
    <VARIABLE id="FEEL" value="dsp.input2"/>
    <VARIABLE id="PURIFY" value="dsp.input3"/>
    <VARIABLE id="GLIDE" value="dsp.input4"/>
    <VARIABLE id="ELECTRIFY" value="dsp.input5"/>
	<VARIABLE id="STRICT" value="dsp.input6"/>
	<VARIABLE id="ALGOMODE" value="dsp.input7"/>
    <VARIABLE id="MUTE" value="dsp.input8"/>
    <VARIABLE id="XCLUDE" value="dsp.input9"/>
	<VARIABLE id="MIDIMAP" value="dsp.input10"/>
	<VARIABLE id="EXTMIDI" value="dsp.input11"/>
    <VARIABLE id="INPUTTUNING" value="dsp.input12"/>
    <VARIABLE id="OUTPUTTUNING" value="dsp.input13"/>
    <VARIABLE id="LOW_KEY" value="dsp.input14"/>
    <VARIABLE id="HIGH_KEY" value="dsp.input15"/>
    
	<VARIABLE id="ROUNDING_MODE" value="dsp.input16"/>
	<VARIABLE id="REPEAT" value="dsp.input17"/>
	<VARIABLE id="GLOBAL_THRES" value="dsp.input18"/>
	<VARIABLE id="LOAD_SNAPSHOT" value="dsp.input19"/>
	<VARIABLE id="KEYB_OCTAVE" value="dsp.input20"/>
    
    <!-- Scales and Keys definition-->
    <VARIABLE id="TRANSFORM_SCALES" value="Chromatic;Major;Natural Minor;Harmonic Minor;Melodic Minor;Lydian;Mixolydian;Ciprian;Ciprian Minor;Phrygian;Phrygian Dominant;Dorian;Locrian;Altered;Pentatonic Major;Pentatonic Minor;Pentatonic Egyptian;Pentatonic Blues Major;Pentatonic Blues Minor;Sakura;Wholetone;Half-Whole Diminished;Whole-Half Diminished;Inverse"/>
    <VARIABLE id="TRANSFORM_KEYS" value="C;C#/Db;D;D#/Eb;E;F;F#/Gb;G;G#/Ab;A;A#/Bb;B"/>
    <VARIABLE id="TRANSFORM_SCALES_COUNT" value="0"/>
    <REPEAT index_list="$TRANSFORM_SCALES$">
        <VARIABLE id="TRANSFORM_SCALES_COUNT" override="true" formula="$TRANSFORM_SCALES_COUNT$+1"/>
    </REPEAT>
    <VARIABLE id="TRANSFORM_KEYS_COUNT" value="0"/>
    <REPEAT index_list="$TRANSFORM_KEYS$">
        <VARIABLE id="TRANSFORM_KEYS_COUNT" override="true" formula="$TRANSFORM_KEYS_COUNT$+1"/>
    </REPEAT>
    
    <!-- fake stuff -->

    <!-- These parameters are used just to notify the main custom view, absolute values are not used -->
    <PARAM id="reset_param" type="boolean" default="0"/>
    <PARAM id="shift_semi_param_up" type="boolean" default="0"/>
    <PARAM id="shift_semi_param_down" type="boolean" default="0"/>
    <PARAM id="add_semi_param_up" type="boolean" default="0"/>
    <PARAM id="add_semi_param_down" type="boolean" default="0"/>
    
    <PARAM id="dummy"/>
    
    <!-- Key Transform macros -->
    <PARAM id="root_key" type="enumeration" enum_values="$TRANSFORM_KEYS$"/>
    <PARAM id="scale" type="enumeration" enum_values="$TRANSFORM_SCALES$"/>
    <REPEAT count="$TRANSFORM_KEYS_COUNT$">
        <FORMULA_PARAM id="root_key_menu_item$index$_checked" type="boolean" formula="root_key==$index$"/>
    </REPEAT>
    <REPEAT count="$TRANSFORM_SCALES_COUNT$">
        <FORMULA_PARAM id="scale_menu_item$index$_checked" type="boolean" formula="scale==$index$"/>
    </REPEAT>

  	<VARIABLE id="RESET" value="reset_param"/>
	<VARIABLE id="ROOTKEY" value="root_key"/>
	<VARIABLE id="SCALE" value="scale"/>
	<VARIABLE id="ROTATER" value="shift_semi_param_up"/>
	<VARIABLE id="ROTATEL" value="shift_semi_param_down"/>
	<VARIABLE id="TRUP" value="add_semi_param_up"/>
	<VARIABLE id="TRDOWN" value="add_semi_param_down"/>

    <!-- The 8 Snapshots Actions-->
    <REPEAT index_list="A;B;C;D;E;F;G;H">
        <ACTION type="PITCHMAP_SAVESNAPSHOT_ACTION" id="load_save_snapshot$index$" snapshot_id="$index$"/>
    </REPEAT>
    <PARAM id="snapshot_save_state" type="boolean" default="0"/>
    
    <!-- Auto Update-->
    <PARAM id="new_version_cmd" type="integer" min="-1" max="3" default="0" persistent="false" />
	<ACTION id="DisplayVersionUpToDate" type="DisplayMessageBox" title="$PLUGIN_NAME$" message="The latest Version of the plugin is installed." />
	<ACTION id="DisplayNewVersion" type="DisplayMessageBox" title="$PLUGIN_NAME$" message="A newer Version is available." button0="Cancel" button1="Download" result_param_id="new_version_cmd" />

    <!-- =========================================================================================================== -->
    <!-- helper tags for platform differentiation -->

    <DEFINE>
        <IF_MAC base_type="REPEAT" count="$OS_MAC$"/>
    </DEFINE>

    <DEFINE>
        <IF_WIN base_type="REPEAT" count="$OS_WIN$"/>
    </DEFINE>

    <TEMPLATE id="SYSVAR" mac="#UNDEFINED#" win="#UNDEFINED#">
        <IF_MAC>
            <VARIABLE id="$id$" value="$mac$"/>
        </IF_MAC>
        <IF_WIN>
            <VARIABLE id="$id$" value="$win$"/>
        </IF_WIN>
    </TEMPLATE>

    <!-- variable number of tabulator characters depending on platform -->
    <VARIABLE id="tab_version" value="&#9;"/>
    <SYSVAR id="tab_other" mac="&#9;&#9;" win="&#9;"/>
    
</DUMMY>