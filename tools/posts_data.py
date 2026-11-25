"""Every post of the first four weeks: what it is, where it stands, its caption (in Graham's
voice: no contractions, no abbreviations) and the alt text for each slide."""

TAGS = "#Jesus #healing #prayer #Bible #faith"
LINK = "There is a free prayer for tonight at the link in my profile. Keep seeing your doctor."

def how_alt():
    return ("When someone is sick. 1. Read the verse aloud. It is what God has said. 2. Pray the prayer. "
            "Say their name where the line is. 3. Expect Him to do what He said. And when a healing comes, "
            "have it confirmed by a doctor, and give the glory to Jesus.")

def close_alt(invite):
    return ("Jesus is the healer. " + ("Who came to mind? Send this to them. " if invite else "")
            + "Keep seeing your doctor. HowToPrayForTheSickAndExpectAMiracle.com. Scripture: Berean Standard Bible.")

POSTS = [
  {"week": 0, "day": "Pinned first", "kind": "Brian's video", "status": "Posted. Needs Brian's yes in writing before it is pinned",
   "state": "wait", "files": [],
   "caption": "This is my friend Brian, outside the shops, the day after I prayed for his leg.\n\n"
              "In a car outside a train station I laid a hand on his knee and asked Jesus for a miracle. "
              "A week later his doctor was struggling to explain what had happened.\n\n"
              "His story opens my book, How to Pray for the Sick and Expect a Miracle.\n\n"
              "Keep seeing your doctor, as Brian did.\n\nJesus is the healer.\n\n#Jesus #healing #prayer #testimony #faith",
   "note": "A draft for you to correct: the car, the train station, the knee and the doctor come from the book's description. Change anything that is not exactly so."},

  {"week": 1, "day": "Monday", "kind": "Stand on this · Reel", "status": "Made. Waiting for your voice",
   "state": "voice", "video": "reel/week-1-monday_reel_stand-on-this_mark-1-41_1080x1920_DRAFT-no-voice-yet.mp4",
   "poster": "reel/week-1-monday_reel_cover_1080x1920.jpg",
   "caption": "When you wonder if He is willing.\n\n"
              "A man with leprosy knelt in front of Jesus and said, “If You are willing, You can make me clean.” "
              "Jesus reached out His hand and touched him. “I am willing,” He said. “Be clean!” (Mark 1:40–41)\n\n"
              "He has not changed.\n\n" + LINK + "\n\n" + TAGS,
   "note": "No sound yet. The words come in phrase by phrase at your reading pace. When you attach audiobook file 19 (Healing Scriptures) or file 05 (Chapter One), I cut your reading of Mark 1:41 and your “Jesus is the healer.” from file 23, and set each phrase to land on your voice."},

  {"week": 1, "day": "Tuesday", "kind": "A prayer · Reel", "status": "Waiting for audiobook file 04",
   "state": "wait", "files": [],
   "caption": "The prayer that comes out of me when I lay hands on someone who is sick.\n\n"
              "It starts with what God has said. It asks plainly. It expects Him to do it, right now, "
              "in the name of Jesus Christ of Nazareth.\n\n" + LINK + "\n\n" + TAGS,
   "note": "A change from the plan, so you need not record anything new: use “How I pray”, the prayer you already read in the audiobook (file 04, A Word Before We Begin), about thirty seconds, with the words on screen."},

  {"week": 1, "day": "Thursday", "kind": "Swipe and keep · Carousel", "status": "Ready to post",
   "state": "ready", "dir": "week-1-when-you-wonder-if-he-is-willing",
   "caption": "A prayer for when you wonder if He is willing.\n\n"
              "Read the verse aloud. It is what God has said. Then pray the prayer, and say their name where the line is.\n\n"
              + LINK + "\n\n" + TAGS,
   "alt": ["When you wonder if He is willing. God’s Word to stand on, and a prayer ready to pray.",
           "Stand on this. Moved with compassion, Jesus reached out His hand and touched the man. “I am willing,” He said. “Be clean!” Mark 1:41.",
           "Pray this. Lord Jesus, You were willing then, and You have not changed. I bring, a line for their name, to You. I ask You to heal them, in the name of Jesus Christ of Nazareth. Amen. Jesus is the healer.",
           how_alt(), close_alt(True)]},

  {"week": 1, "day": "Saturday", "kind": "Film 1, “I am willing” · Reel", "status": "Film approved. Caption ready",
   "state": "ready", "files": [],
   "caption": "A man with leprosy came to Jesus and said, “If You are willing, You can make me clean.” "
              "Jesus touched him. “I am willing,” He said. “Be clean!” (Mark 1:40–42)\n\n"
              "If you are still sick, you are not to blame, and you are not forgotten. "
              "There is a prayer you can pray tonight, free. The link is in my profile.\n\n"
              "The story is told in the words of the Bible (Mark 1:40–42, Berean Standard Bible). "
              "Pictures and voices made with artificial intelligence. Keep seeing your doctor.\n\n" + TAGS,
   "note": "Post the Instagram master of version 20 with the cover frame, and switch on “Label as made with AI”. If the film is re-voiced with your reading, change the last paragraph to “Pictures made with artificial intelligence. Read by Graham Marsland.”"},

  {"week": 2, "day": "Thursday", "kind": "Swipe and keep · Carousel", "status": "Ready to post",
   "state": "ready", "dir": "week-2-when-you-need-something-to-stand-on",
   "caption": "A prayer for when you need something to stand on.\n\n"
              "“By His stripes you are healed.” (1 Peter 2:24) It is what God has said, and you can stand on it.\n\n"
              "Read the verse aloud. Then pray the prayer, and say their name where the line is.\n\n" + LINK + "\n\n" + TAGS,
   "alt": ["When you need something to stand on. God’s Word to stand on, and a prayer ready to pray.",
           "Stand on this. He Himself bore our sins in His body on the tree, so that we might die to sin and live to righteousness. “By His stripes you are healed.” 1 Peter 2:24.",
           "Pray this. Father, thank You for the cross. You have said that by His stripes we are healed, and I stand on what You have said. I ask You to heal, a line for their name, in the name of Jesus Christ of Nazareth. Amen. Jesus is the healer.",
           how_alt(), close_alt(False)]},

  {"week": 3, "day": "Thursday", "kind": "Swipe and keep · Carousel", "status": "Ready to post",
   "state": "ready", "dir": "week-3-when-you-do-not-know-what-to-pray",
   "caption": "A prayer for when you do not know what to pray.\n\n"
              "Jesus asked a blind man, “What do you want Me to do for you?” The man did not hint. "
              "He told Jesus plainly what he wanted. (Mark 10:51)\n\n"
              "You can ask plainly too. Read the verse aloud, then pray the prayer, and say what you are asking where the line is.\n\n"
              + LINK + "\n\n" + TAGS,
   "alt": ["When you do not know what to pray. God’s Word to stand on, and a prayer ready to pray.",
           "Stand on this. “What do you want Me to do for you?” Jesus asked. “Rabboni,” said the blind man, “let me see again.” Mark 10:51.",
           "Pray this. Lord Jesus, You asked a blind man what he wanted, and he told You plainly. So I tell You plainly what I am asking. I ask You to, a line for what you are asking. In the name of Jesus Christ of Nazareth. Amen. Jesus is the healer.",
           how_alt(), close_alt(False)]},

  {"week": 4, "day": "Thursday", "kind": "Swipe and keep · Carousel", "status": "Ready to post",
   "state": "ready", "dir": "week-4-if-you-are-still-sick",
   "caption": "If you are still sick, this is for you.\n\n"
              "You are not to blame, and you are not forgotten. Come to Him again today, and ask others to pray with you.\n\n"
              "Keep seeing your doctor. Jesus sent the man He healed to be examined (Mark 1:44).\n\n"
              "There is a free prayer for tonight at the link in my profile.\n\n" + TAGS,
   "alt": ["If you are still sick. A word for you, and God’s Word to stand on.",
           "Stand on this. Let us then approach the throne of grace with confidence, so that we may receive mercy and find grace to help us in our time of need. Hebrews 4:16.",
           "You are not to blame, and you are not forgotten. Jesus is the healer.",
           "For today. Come to Him again today. Ask others to pray with you. Keep seeing your doctor. Jesus sent the man He healed to be examined (Mark 1:44).",
           close_alt(True)]},
]
