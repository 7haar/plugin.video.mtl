import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import xbmcvfs


import time
import json
import os

from resources.lib import utils as u

ADDON = xbmcaddon.Addon()
PROFILE = xbmcvfs.translatePath(ADDON.getAddonInfo('profile'))
DATAFILE = os.path.join(PROFILE, 'resumes.json')
d = xbmcgui.Dialog()

class RPlayer(xbmc.Player):
    def __init__(self, video=None):
        super(RPlayer, self).__init__()
        self.video = video

    def resume(self):
        return

    def onPlayBackStarted(self):
        xbmc.log("[RPlayer] onPlayBackStarted", xbmc.LOGNOTICE)
        # Kurze, nicht-blockierende Wartezeit für sicheren Start
        d.notification("Wiedergabe", "Wiedergabe gestartet", xbmcgui.NOTIFICATION_INFO, 2000)
    
    def onAVStarted(self):
        xbmc.log("[RPlayer] onPlayBackStarted", xbmc.LOGNOTICE)
        # Kurze, nicht-blockierende Wartezeit für sicheren Start
        d.notification("Wiedergabe", "Wiedergabe gestartet", xbmcgui.NOTIFICATION_INFO, 2000)

    def onPlayBackStopped(self):
        xbmc.log("[RPlayer] onPlayBackStopped", xbmc.LOGNOTICE)
        d.notification("Wiedergabe", "Wiedergabe gestoppt", xbmcgui.NOTIFICATION_INFO, 2000)

    def onPlayBackEnded(self):
        xbmc.log("[RPlayer] onPlayBackEnded", xbmc.LOGNOTICE)
        d.notification("Wiedergabe", "Wiedergabe beendet", xbmcgui.NOTIFICATION_INFO, 2000)

    def onPlayBackError(self):
        xbmc.log("[RPlayer] onPlayBackError", xbmc.LOGERROR)
        d.notification("Fehler", "Wiedergabe-Fehler", xbmcgui.NOTIFICATION_ERROR, 3000)    
    
'''

def _load_resumes():
    try:
        with open(DATAFILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_resumes(d):
    os.makedirs(os.path.dirname(DATAFILE), exist_ok=True)
    with open(DATAFILE, 'w') as f:
        json.dump(d, f)
'''

class ResumePlayer(xbmc.Player):
    """
    Resume-fähiger Player:
    - Beim Start: liest Resume aus play_item Property 'resume_time' oder aus JSON (key)
      und führt seekTime aus.
    - Beim Stop/End: speichert aktuellen Time-Position in JSON; bei Ende wird Resume gelöscht.
    Usage:
      player = ResumePlayer(key=unique_key, listitem=play_item)
      player.play(path, listitem=play_item)
    key: eindeutiger Schlüssel für Resume (z.B. Pfad oder Hash)
    listitem: xbmcgui.ListItem, optional (wird für VideoInfoTag genutzt)
    """

    def __init__(self, key, listitem=None):
        super(ResumePlayer, self).__init__()
        self.key = key
        self.listitem = listitem
        #self._resumes = _load_resumes()
        self._seek_done = False

    def _get_stored_resume(self):
        # Priorität: ListItem property 'resume_time' -> JSON entry
        try:
            if self.listitem:
                prop = self.listitem.getProperty('resume_time')
                if prop:
                    return int(prop)
        except Exception:
            pass
        try:
            val = self._resumes.get(self.key)
            if val is not None:
                return int(val)
        except Exception:
            pass
        return None

    def onPlayBackStarted(self):
        xbmc.log(f"[ResumePlayer] onPlayBackStarted key={self.key}", xbmc.LOGNOTICE)
        # set VideoInfoTag Resume if we have a stored resume
        '''
        try:
            pos = self._get_stored_resume()
            if pos is not None and self.listitem:
                try:
                    info = self.listitem.getVideoInfoTag()
                    duration = int(self.listitem.getProperty('duration') or 0)
                    info.setResumePoint(int(pos), duration)
                except Exception:
                    xbmc.log("[ResumePlayer] setResumePoint failed", xbmc.LOGERROR)
            # seek only once after playback actually started
            # Warte kurz bis player.isPlaying()
            timeout = time.time() + 5
            while not self.isPlaying() and time.time() < timeout:
                xbmc.sleep(100)
            if not self._seek_done and pos:
                try:
                    # kleine Verzögerung sicherstellen
                    xbmc.sleep(250)
                    self.seekTime(int(pos))
                    xbmc.log(f"[ResumePlayer] seekTime to {pos}s for {self.key}", xbmc.LOGNOTICE)
                    self._seek_done = True
                except Exception as e:
                    xbmc.log(f"[ResumePlayer] seekTime failed: {e}", xbmc.LOGERROR)
        except Exception as e:
            xbmc.log(f"[ResumePlayer] onPlayBackStarted error: {e}", xbmc.LOGERROR)
        '''
        
    def onPlayBackStopped(self):
        xbmc.log(f"[ResumePlayer] onPlayBackStopped key={self.key}", xbmc.LOGNOTICE)
        '''
        try:
            pos = self.getTime() or 0
            # minimaler Threshold (z. B. ignorieren <30s)
            if pos and int(pos) > 30:
                self._resumes[self.key] = int(pos)
                _save_resumes(self._resumes)
                xbmc.log(f"[ResumePlayer] Saved resume {int(pos)}s for {self.key}", xbmc.LOGNOTICE)
            else:
                # zu kurz -> löschen, falls vorhanden
                if self.key in self._resumes:
                    del self._resumes[self.key]
                    _save_resumes(self._resumes)
                    xbmc.log(f"[ResumePlayer] Cleared resume (too short) for {self.key}", xbmc.LOGNOTICE)
        except Exception as e:
            xbmc.log(f"[ResumePlayer] onPlayBackStopped error: {e}", xbmc.LOGERROR)
        '''

    def onPlayBackEnded(self):
        xbmc.log(f"[ResumePlayer] onPlayBackEnded key={self.key}", xbmc.LOGNOTICE)
        '''
        try:
            # Bei vollständigem Ende Resume entfernen
            if self.key in self._resumes:
                del self._resumes[self.key]
                _save_resumes(self._resumes)
                xbmc.log(f"[ResumePlayer] Cleared resume for {self.key}", xbmc.LOGNOTICE)
        except Exception as e:
            xbmc.log(f"[ResumePlayer] onPlayBackEnded error: {e}", xbmc.LOGERROR)
        '''

    def onPlayBackError(self):
        xbmc.log(f"[ResumePlayer] onPlayBackError key={self.key}", xbmc.LOGERROR)
        # optional: Fehlerbehandlung ähnlich wie onPlayBackStopped


# Beispiel funktion playvideo

def playvideo(path, alt):
    play_item = xbmcgui.ListItem()
    if not check_url(path):
        path = alt
    play_item.setPath(path)

    # optional: Dauer als Property setzen, damit setResumePoint sinnvolle Dauer hat
    # play_item.setProperty('duration', str(int(duration_seconds)))

    # resume_key: eindeutiger identifier (z. B. vollständiger URL oder Hash)
    '''
    resume_key = path

    # Falls du einen zuvor gespeicherten Resumewert kennst und ihn ins ListItem geben willst:
    resumes = _load_resumes()
    if resume_key in resumes:
        play_item.setProperty('resume_time', str(resumes[resume_key]))
    '''
    resume_key = 0
    player = Player(key=resume_key, listitem=play_item)
    ok = player.play(path, listitem=play_item)
    if not ok:
        xbmc.log("player.play returned False, fallback to setResolvedUrl", xbmc.LOGWARNING)
        xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)