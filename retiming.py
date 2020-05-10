import maya.cmds as cmds
import maya.mel as mel


class RetimingTool(object):
    
    @classmethod
    def retime_keys(cls, retime_val, incremental, move_to_next):
        range_start, range_end = cls.get_selected_range()
        start_key = cls.get_start_keyframe_time(range_start)
        last_key = cls.get_last_keyframe_time()
        
        current = start_key
        current_keyframe_values = [start_key]
        new_keyframes = [start_key]
        
        # iterate starting at first key and going to last
        while current != last_key:
            # get the next keyframe
            next_keyframe = cls.find_keyframe("next", current)
            if incremental:
                # get how many frames between keyframes
                diff = next_keyframe - current
                
                # Ensure we are not at the end of the keyframes
                if current < range_end:
                    
                    # calcuate the amount to retime from current key
                    diff += retime_val
                    if diff < 1:
                        diff = 1
            else:
                if current < range_end:
                    # if it is not incremental, we make the difference = to the retime value.
                    diff = retime_val
                else:
                    # Outside selection only moves in releation
                    diff = next_keyframe - current
                    
            # add retime value (diff) to last key in list)
            new_keyframes.append(new_keyframes[-1] + diff)    
            current = next_keyframe
            current_keyframe_values.append(current)
        
        if len(new_keyframes) > 1:
            cls.retime_keys_recursive(start_key, 0, new_keyframes)
    
        first_key = cls.find_keyframe('first')
        
        if move_to_next and range_start >= first_key:
            next_keyframe = cls.find_keyframe('next', start_key)
            cls.set_current_time(next_keyframe)
        elif range_end > first_key:
            cls.set_current_time(start_key)
        else:
            cls.set_current_time(range_start)
          
                
    @classmethod
    def retime_keys_recursive(cls, current_time, index, new_keyframe_times):
        
        # base case
         if index >= len(new_keyframe_times):
             return
                 
         
         updated_keyframe_time = new_keyframe_times[index]
         next = cls.find_keyframe('next', current_time)
         
         if updated_keyframe_time < next:
             # update the keyframe
             cls.change_keyframe_time(current_time, updated_keyframe_time)
             #recusive to next keyframe
             cls.retime_keys_recursive(next, index + 1, new_keyframe_times)
         else:
             # not safe to move, continue to next
             cls.retime_keys_recursive(next, index + 1, new_keyframe_times)
             # recusion loops back to this once it is safe to move.
             cls.change_keyframe_time(current_time, updated_keyframe_time)
         
         
    
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
    print(RetimingTool.retime_keys(2, False, True))
    
