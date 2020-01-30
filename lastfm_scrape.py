import requests
import json
import csv
import re
from app import db
from app.models import Answer


url = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&'
param = {"api_key" : 'API-KEY', "limit": 10, "format": "json"}

count = 1

with open('song_number.csv', mode='r') as csv_file:
    readcsv = csv.reader(csv_file, delimiter=',')
    for row in readcsv:
        full = row[0].split('_')
        ans_full = full[1].split('-')
        samp_num = row[1]
        ans_art = ans_full[0]
        ans_art = ans_art.strip()
        ans_song = ans_full[1]
        ans_song = ans_song.strip()

        param["artist"] = ans_art
        param["track"] = ans_song

        source = requests.get(url, params=param)

        rel_data = []
        print(count)
        lastfm_data = source.json()
        try:    
            lastfm_data = lastfm_data['similartracks']["track"]

            for info in lastfm_data:
                lfm_art = info['artist']['name']
                lfm_song = info['name']
                full_lfm = lfm_art + " - " + lfm_song
                rel_data.append(full_lfm)

            rel_data = ','.join(map(str, rel_data))

            db.session.query(Answer).filter(Answer.id == count).update({'answers': rel_data})
        except:
            pass
        
        count = count + 1


db.session.commit()

#[7, 12, 14, 43, 67, 69, 89, 92, 107, 121, 125]
#["Jean Knight - Why I Keep Living These Memories,The Dells - All Your Goodies Are Gone,The Temptations - Gonna Keep On Tryin' Till I win Your Love,The Stylistics - My Funny Valentine,The Emotions - Blind Alley,Jerry Butler - Just Because I Really Love You,The Charmels - As Long as I Have You,Jerry Butler - No Money Down,Bobby Byrd - I'm Not To Blame,Minnie Riperton - When It Comes Down To It",
# "Don Harper - Chamber Pop,Keff McCulloch - The White Flag,Keff McCulloch - Here's to the Future,Brian Hodgson - Nightwalker,Brian Hodgson - Quest,Mark Ayres - Tubular Bells,Mark Ayres - Crockett's Theme,Murray Gold - Doomsday,Murray Gold - The Long Song",
# "Major Harris - What's The Use In The Truth,Major Harris - Walkin' in the footsteps,Barry White - Break It Down With You,The Whispers - Creation of Love,The Stylistics - I plead guilty,The Stylistics - Put a little love away,The Whispers - Planets of Life,Barry White - Mellow Mood (part 1),The Moments - Lucky Me,The Emotions - Yes, I Am",
# "Tom Brock - I Love You More And More (Album Version),Tom Brock - I Love You More & More,Jackson Sisters - Boy, You're Dynamite,Barry White - I Only Want To Be With You,Chic - Would You Be My Baby,Marvin Gaye - Got to Give It Up, Part 1,Bobby Thurston - You Got What It Takes (Instrumental),Bobby Thurston - Check out the groove (12 Inch),Bobby Thurston - I Wanna Do It for You,Bobby Thurston - Check Out the Groove [Instrumental],George McCrae - I Get Lifted",
# "Janet Jackson - Because of Love,Janet Jackson - That's the Way Love Goes,Aaliyah - Rock the Boat,Aaliyah - It's Whatever,TLC - Diggin' on You,Ciara - Body Party,Mariah Carey - Breakdown,Mariah Carey - Honey,TLC - Red Light Special,Toni Braxton - Another Sad Love Song",
# "Ween - How High Can You Fly,Chrome - SS Cygni,Psychic TV - BB,Sun City Girls - Esoterica of Abyssynia,Brainbombs - After Acid,White Noise - Your Hidden Dreams,White Noise - Love Without Sound,Chrome - You’ve Been Duplicated,The Legendary Pink Dots - Tower 4,The Legendary Pink Dots - Madame Guillotine", 
# "24-Carat Black - FOODSTAMPS,24-Carat Black - Poverty's Paradise,Frederick Knight - Lean On Me,Frederick Knight - Now That I've Found You,Boscoe - If I Had My Way,Boscoe - I'm What You Need,Isaac Hayes - Joy,Funkadelic - This Broken Heart,Isaac Hayes - Soulsville,Funkadelic - Back in Our Minds",
# "The Heath Brothers - Move To The Groove,The Heath Brothers - Then What,The Heath Brothers - Use It (Don't Abuse It),24-Carat Black - FOODSTAMPS,The New Orleans Banjo Band - The Darktown Strutter's Ball,The New Orleans Banjo Band - Ja-Da,Jay Berliner - Stormy,Jay Berliner - Adelita & Lagrina,Jay Berliner - Korky the Cat,Jay Berliner - Für Elise",
# "Marco Beltrami - Main Title,Joe Kraemer - The Way of the Gun,Christopher Gordon - The Statue & The Dance Of The Ghouls,Alfred Newman - The First Kiss,Miklós Rózsa - Main Title,Miklós Rózsa - Spellbound,Max Steiner - The Adventure Begins,Gabriel Yared - Sinking Ship,Elliot Goldenthal - Silver Screen Kiss,Gabriel Yared - 10 Haunted Hotels",
# "The Isley Brothers - Groove With You,Harold Melvin & The Blue Notes - I Miss You,The Isley Brothers - Voyage To Atlantis,The O'Jays - Forever Mine,Rufus - Sweet Thing,Bobby Womack - If You Think You're Lonely,Earth, Wind & Fire - Devotion,Luther Vandross - SUPERSTAR / UNTIL YOU COME BACK TO ME (THAT'S WHAT I'M GONNA DO),Average White Band - A Love of Your Own,The O'Jays - Lovin' You",
# "Barry Gray - Stingray,Barry Gray - ThunderBirds,Eugene Raskin; Lou Singer - Gigantor,Albert P. Brodax - Cool McCool,Treadwell Covington; Joseph Harris; Chester Stover - The Go-Go Gophers,W. Watts Biggers - The World of Commander McBragg,Joseph Barbera; William Hanna - Secret Squirrel,Joseph Barbera; William Hanna - The Atom Ant Show,Joseph Barbera; William Hanna - Wacky Races,Joseph Barbera; Hoyt Curtin; William Hanna - Hong Kong Phooey"]



