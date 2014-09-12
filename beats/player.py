import vlc

instance = vlc.Instance('--no-video')
player = instance.media_player_new()
now_playing = None
volume = 100


def play(mrl):
    m = instance.media_new(mrl)
    player.set_media(m)
    player.play()
    return get_status()


def play_media(media):
    play(media.mrl())
    global now_playing
    now_playing = media
    return get_status()


def pause():
    player.pause()
    return get_status()


def stop():
    player.stop()
    global now_playing
    now_playing = None
    return get_status()


def get_status():
    media = player.get_media()
    status = {'state': str(player.get_state()), 'volume': volume}
    if media:
        status['media'] = vlc.bytes_to_str(media.get_mrl())
        status['current_time'] = player.get_time()
        status['duration'] = media.get_duration()
    return status


def get_now_playing():
    obj = {'player_status': get_status()}
    if now_playing:
        obj['media'] = now_playing.dictify()
    return obj


def set_volume(vol):
    global volume
    volume = vol
    player.audio_set_volume(vol)
    return get_status()


def has_ended():
    return player.get_state() in [
        vlc.State.Ended,
        vlc.State.Stopped,
        vlc.State.NothingSpecial,
        vlc.State.Error,
    ]


def is_youtube_video(m=None):
    if m is None:
        m = player.get_media()
    mrl = vlc.bytes_to_str(m.get_mrl())
    return m is not None and 'http://www.youtube.com' in mrl


def get_vlc_version():
    return vlc.libvlc_get_version()
