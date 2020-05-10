import maya.cmds as cmds
import maya.mel as mel


class RetimingTool(object):
    
    @classmethod
    def set_current_time(cls, time):
        cmds.currentTime(time)
    
    @classmethod
    def get_selected_range(cls):
        playback_slider = mel.eval("$tempVar = $gPlayBackSlider")
        range = cmds.timeControl(playback_slider, q=True, rangeArray=True)
        return range
        
    @classmethod
    def find_keyframe(cls, which, time=None):
        kwargs = {"which":which}
        if which in ["next", "previous"]:
            kwargs['time'] = (time, time)
        return cmds.findKeyframe(**kwargs)
    @classmethod
    def change_keyframe_time(cls, current_time, new_time):
        cmds.keyframe(e=True, time=(current_time, current_time), timeChange=new_time)
        
    @classmethod
    def get_start_keyframe_time(cls, range_start_time):
        start_times = cmds.keyframe(q=True, time=(range_start_time, range_start_time))
        if start_times:
            return start_times[0]
        start_time = cls.find_keyframe("previous", range_start_time)
        return start_time
        
    @classmethod
    def get_last_keyframe_time(cls):
        return cls.find_keyframe("last")
        
        
if __name__ == '__main__':
    print(RetimingTool.get_last_keyframe_time())
