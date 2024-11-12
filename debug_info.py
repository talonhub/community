
from talon import actions, speech_system
def print_timings(j):
    meta = j['_metadata']
    status  = f"[audio]={meta['audio_ms']:.3f}ms "
    status += f"[compile]={meta['compile_ms']:.3f}ms "
    status += f"[emit]={meta['emit_ms']:.3f}ms "
    status += f"[decode]={meta['decode_ms']:.3f}ms "
    
    if meta['reject']:
        print(f"Rejected: {meta['emit']}")

    status += f"[total]={meta['total_ms']:.3f}ms "
    print(status)
speech_system.register('phrase', print_timings)
