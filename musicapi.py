from ytmusicapi import YTMusic

ytmusic = YTMusic()
mainsongartists = {}

def get_song_recommendation(emotion):
    global mainsongartists
    if(emotion):
        mapper ={
            'canthearloud':'calm soothing classical hindustani',
            'happy': 'lover',
            'neutral': 'Enjoy enjaami',
            'joy': 'guruvara sanje song',
            'angry': 'look at me! rap',
            'surprise': 'eye of the tiger survivor',
            'rock': 'rock song',
            'yoyo': 'tauba tauba song',
            'sad': 'male ninthu hoda mele',
            'depressed': 'moye more official video song'
        }
        search = mapper[emotion]
        
        search_results = ytmusic.search(search, filter="songs", limit=1)
        first_song = search_results[0]
        video_id = first_song.get('videoId')
        mainsongartists = first_song
        return continue_recommendation(video_id)

def continue_recommendation(videoid):
    mainsong = ytmusic.get_song(videoid)

    #3 similar songs
    watch_section = ytmusic.get_watch_playlist(videoId=videoid, limit=3, radio=False)
    similar1 = ''
    similar2 = ''
    similar3 = ''
    relatedsongs=''
    if 'related' in watch_section:
        browse_id = watch_section['related']
        relatedsongs = ytmusic.get_song_related(browse_id)
        similar1 = relatedsongs[0]['contents'][0:1][0]
        similar2 = relatedsongs[0]['contents'][1:2][0]
        similar3 = relatedsongs[0]['contents'][2:3][0]
        #"url": songurl.get('url'),
    return_songs_data = {
        "mainsong":{
            "title": mainsong['videoDetails'].get("title"),
            "artist": ", ".join([artist["name"] for artist in mainsongartists.get("artists", [])]),
            "coverart": mainsong['videoDetails']['thumbnail'].get("thumbnails", [{}])[-1].get("url"),
            "videoid": videoid,
            },
        "similar1":{
            "title": similar1.get("title"),
            "artist": ", ".join([artist["name"] for artist in similar1.get("artists", [])]),
            "coverart": similar1.get("thumbnails", [{}])[-1].get("url"),
            "videoid": similar1.get("videoId"),
            },
        "similar2":{
            "title": similar2.get("title"),
            "artist": ", ".join([artist["name"] for artist in similar2.get("artists", [])]),
            "coverart": similar2.get("thumbnails", [{}])[-1].get("url"),
            "videoid": similar2.get("videoId"),
            },
        "similar3":{
            "title": similar3.get("title"),
            "artist": ", ".join([artist["name"] for artist in similar3.get("artists", [])]),
            "coverart": similar3.get("thumbnails", [{}])[-1].get("url"),
            "videoid": similar3.get("videoId"),
            }
    }
    return return_songs_data
    
