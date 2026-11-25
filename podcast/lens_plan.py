"""The podcast, rebuilt around the people who listen (26 November 2026).

Graham, 8:22 am: "I don't want it to follow exactly the chapters of the book. I think that's boring.
Let's just follow the lenses of people that would be interested in this subject and target it
based on the various lenses."

Eight lenses, three episodes each in the first 24, rotating so that no two neighbouring
episodes speak to the same person. Every episode: one listener, one question in that person's
own words, one outcome, three things to build on, one ending. The hosts are given ONLY the book's
own text for that episode (the clean "Chapter ..." sources). Every instruction goes in the
customise box, never in a source.

Writes lens_episodes.json (used by the notebook helpers, the covers and the website kit).
"""
import json, pathlib

LENSES = {
    "A": "When you are the one who is sick",
    "B": "When your child is sick",
    "C": "When you are caring for someone",
    "D": "When you have never prayed for anyone",
    "E": "When you are still waiting",
    "F": "When you are not sure God still heals",
    "G": "When you lead others",
    "H": "When you are getting to know Jesus",
}

# key of each clean source in the notebook -> the start of its name there
PART_NAME = {"00": "A Word Before We Begin:", "15": "Healing Scriptures to Stand On"}
for i, w in enumerate(["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                       "Eleven", "Twelve", "Thirteen", "Fourteen"], start=1):
    PART_NAME[f"{i:02d}"] = f"Chapter {w}:"

PRAYER = {
    "00": "Father, thank You for the person holding this book.",
    "01": "Father, thank You that You are the LORD who heals.",
    "02": "Lord Jesus, thank You for the cross.",
    "03": "Lord Jesus, thank You that You did not leave this work to a gifted few.",
    "04": "Father, thank You that Your Word is living and active.",
    "05": "Father, thank You that You love it when I ask.",
    "06": "Lord Jesus, I do not want to be like Nazareth.",
    "07": "Father, I have faith in You.",
    "08": "Father, I confess that I have been afraid of looking foolish.",
    "09": "Lord Jesus, thank You for Your name, the name above every name.",
    "10": "Lord Jesus, thank You for Your compassion.",
    "11": "Father, thank You that healing is not complicated.",
    "12": "Lord Jesus, thank You for every story of Your goodness.",
    "13": "Father, I bring You my disappointments.",
    "14": "Lord Jesus, here I am.",
}

# n, lens, title, listener, outcome, sources, three priorities, prayer source, Scripture (cover),
# picture key (make_covers.py), one line for the website, words that must be in the ticked text
E = [
 (1, "A", "Does God Want Me Well?",
  "someone who is sick right now. They love Jesus, but they are tired and frightened, and deep down they wonder whether God really wants them well",
  "that they leave knowing, from the Bible, that healing is part of who God is",
  ["01"],
  ["The bitter water at Marah, and the name God gave Himself there: “I am the LORD who heals you” (Exodus 15:26). Read the verse aloud.",
   "What the book says under “His Name Is Healer”, and Psalm 103:2-3, read aloud.",
   "What the book says under “Where Sickness Fits”, said gently."],
  "01", "Exodus 15:26", "marah",
  "At Marah the water was too bitter to drink, and there God told His people one of His names: “I am the LORD who heals you.” For anyone who is sick and wonders whether God wants them well.",
  ["Marah", "Exodus 15:26", "His Name Is Healer", "Psalm 103:2", "Where Sickness Fits"]),
 (2, "B", "How Do I Pray for My Child When I Am Frightened?",
  "a mother or father whose child is sick. They are frightened, they love Jesus, and they are not sure their faith is strong enough",
  "that they know they can bring their child to Jesus honestly, fear and all",
  ["07"],
  ["The father who brought his son to Jesus and cried out, “I do believe; help my unbelief!” (Mark 9:24), and how Jesus answered him.",
   "What the book says about faith facing the facts, with Abraham (Romans 4:19-21): honest about what you see, and still holding on to what God has said.",
   "The book's words “God is good, His Word is true”, offered gently as an invitation, never as a burden."],
  "07", "Mark 9:24", "flame",
  "A father brought his son to Jesus and cried out, “I do believe; help my unbelief!” For every parent who is frightened for their child.",
  ["Mark 9:24", "Romans 4:19", "God is good"]),
 (3, "C", "What Do I Say When I Pray for Someone I Love?",
  "someone caring for a husband, wife, parent or friend who is sick, at home or beside a hospital bed. They want to pray with the person they love but do not know what to say or do",
  "that they could pray for the person they love tonight, simply and kindly",
  ["11", "12"],
  ["Graham praying for his friend Brian in the car, as the book tells it under “My Friend Brian” and “In the Car”.",
   "The first five steps of the simple model in the book: ask permission, ask what they need, lay hands with honour, pray the Word and ask, speak in the name of Jesus. Keep each one short and practical.",
   "James 5:14-15. Read it aloud."],
  "11", "James 5:14–15", "oil",
  "A simple, kind way to pray for someone you love, one step at a time, and a prayer Graham prayed for his friend in a car.",
  ["My Friend Brian", "In the Car", "Ask Permission", "James 5:14"]),
 (4, "D", "Is It Really My Place to Pray for the Sick?",
  "an ordinary Christian who has never prayed out loud for someone who is sick. They feel nervous and unqualified, and they think this is only for pastors or people with a special gift",
  "that they see Jesus gave this to every believer, including them",
  ["03", "00"],
  ["Ananias, an ordinary follower of Jesus, sent to lay his hands on Saul (Acts 9), as the book tells it.",
   "Jesus' words in Mark 16:17-18 and John 14:12, read aloud, and what the book says under “You Are Qualified” and “This Book Is for You”.",
   "“Why Hands?”: a gentle hand on the shoulder, always with permission."],
  "03", "Mark 16:17–18", "people",
  "Ananias was an ordinary follower of Jesus when God sent him to lay his hands on Saul. For anyone who thinks praying for the sick is only for pastors.",
  ["Ananias", "Mark 16:17", "John 14:12", "You Are Qualified", "This Book Is for You", "Why Hands"]),
 (5, "E", "Is It My Fault I Am Still Sick?",
  "someone who has prayed, perhaps for a long time, and is still sick. Someone may have told them they did not have enough faith. They are tired, and afraid it is their fault",
  "that they hear clearly that they are not to blame, that God has not forgotten them, and that it is right to keep asking",
  ["13"],
  ["What the book says under “Never Blame the Sick”. Say it plainly and kindly.",
   "“Even the Disciples”: the boy the disciples could not help, and how that was never the fault of the boy or his father.",
   "“The Things We Do Not Understand”, and Galatians 6:9: let us not grow weary. Read it aloud."],
  "13", "Galatians 6:9", "sunrise",
  "For anyone who has prayed and is still sick. Why a person who is still sick is never to blame, and why it is right to keep asking.",
  ["Never Blame the Sick", "Even the Disciples", "The Things We Do Not Understand", "Galatians 6:9"]),
 (6, "F", "Does God Still Heal Today?",
  "a Christian who loves Jesus but is not sure God still heals today. Perhaps they were taught that healing ended with the apostles, or they have been put off by healing shows on television",
  "that they hear an honest, humble account and see that every story points to Jesus",
  ["12"],
  ["“The Woman Who Walked Against the Crowd”: the young woman in Perth, told exactly as the book tells it, adding nothing.",
   "The woman in the Gospel who pushed through the crowd to touch Jesus (Mark 5:27-28), and “Her Faith Came First”.",
   "“All the Glory to Jesus”: Graham did not heal anyone; he asked, and Jesus did what He said He would do. Read Acts 4:20 aloud."],
  "12", "Acts 4:20", "crowd",
  "An honest account of a young woman in Perth, as the book tells it, and why every story like it points to Jesus.",
  ["Walked Against the Crowd", "Perth", "Mark 5:27", "Her Faith Came First", "All the Glory to Jesus", "Acts 4:20"]),
 (7, "G", "How Do I Lead My Church to Pray for the Sick?",
  "a pastor, small-group leader or member of a prayer team who wants to lead people to pray for the sick with love, honour and good sense",
  "that they have a simple, kind way to start this month",
  ["14", "11"],
  ["The seventy-two whom Jesus sent out two by two (Luke 10), and Matthew 10:7-8, read aloud.",
   "The simple model in the book, especially asking permission, honouring the person, checking gently, and encouraging a doctor to confirm any healing.",
   "“Signs Point Somewhere” and “Tell Your Story”: everything points to Jesus, and no one is pressured or blamed."],
  "14", "Matthew 10:7–8", "road",
  "Jesus sent seventy-two of His followers out two by two. A simple, kind way for a church or a small group to begin praying for the sick.",
  ["seventy-two", "Matthew 10:7", "Signs Point Somewhere", "Tell Your Story", "Ask Permission"]),
 (8, "H", "What Is Jesus Like?",
  "someone who is still finding out who Jesus is. They may not go to church. They want to know whether He would care about someone like them",
  "that they meet Jesus in the story and know they can call out to Him too",
  ["05"],
  ["Blind Bartimaeus, who kept shouting when the crowd told him to be quiet, and how Jesus stopped for him (Mark 10:46-52), as the book tells it under “The Blind Man Who Shouted”.",
   "Jesus' question, “What do you want Me to do for you?” (Mark 10:51). Read it aloud.",
   "“Ask Honestly” and “Ask Now”: you do not have to get everything right before you come to Him."],
  "05", "Mark 10:51", "eye",
  "Blind Bartimaeus kept calling out when the crowd told him to be quiet, and Jesus stopped. For anyone still finding out who Jesus is.",
  ["Bartimaeus", "The Blind Man Who Shouted", "Mark 10:51", "Ask Honestly", "Ask Now"]),
 (9, "A", "What Do I Hold On To When the Symptoms Shout?",
  "someone who is sick and has asked God for healing, but the pain, the test results or the symptoms seem louder than God's promise",
  "that they know how to hold on to what God has said, while being honest about how they feel",
  ["04", "15"],
  ["The Roman centurion who told Jesus, “just say the word” (Matthew 8:5-13), as the book tells it.",
   "Psalm 107:20, read aloud, and what the book says under “It Never Comes Back Empty” and “When the Symptoms Shout”.",
   "How to pray with the Bible open: one promise from “Healing Scriptures to Stand On”, read aloud slowly."],
  "04", "Psalm 107:20", "bible",
  "A Roman centurion told Jesus, “just say the word.” For anyone whose symptoms seem louder than God's promise.",
  ["centurion", "just say the word", "Psalm 107:20", "It Never Comes Back Empty", "When the Symptoms Shout"]),
 (10, "B", "Does God Love My Child More Than I Do?",
  "a mother or father with a sick child, who would do anything to make their child well and wonders whether God feels the same way",
  "that they see God as a Father who loves to give good things, and that they come to Him as His child, not as a beggar",
  ["05"],
  ["Jesus' words in Matthew 7:11: if you know how to give good gifts to your children, how much more will your Father in heaven. Read it aloud.",
   "What the book says under “A Child, Not a Beggar”, and King Hezekiah, who prayed and heard God's answer (2 Kings 20:5).",
   "“Ask Honestly”: tell God plainly what you want for your child."],
  "05", "Matthew 7:11", "bread",
  "If you know how to give good gifts to your children, how much more will your Father in heaven? For every parent of a sick child.",
  ["Matthew 7:11", "A Child, Not a Beggar", "Hezekiah", "Ask Honestly"]),
 (11, "C", "How Do I Love Them Well While They Are Sick?",
  "someone looking after a person they love who is sick, perhaps for a long time. They are tired, and they want to care for them the way Jesus would",
  "that they see how Jesus treated sick people, and know how to honour the person they care for",
  ["10"],
  ["Jesus taking the blind man by the hand and leading him out of the village (Mark 8:23), as the book tells it.",
   "“People, Not Projects” and “Love Honours”: the person who is sick is someone to love, never a project.",
   "1 Corinthians 13:2, read aloud, and “Love Keeps Going”."],
  "10", "1 Corinthians 13:2", "hand-in-hand",
  "Jesus took a blind man by the hand and led him out of the village. For anyone caring for someone they love.",
  ["by the hand", "Mark 8:23", "People, Not Projects", "Love Honours", "1 Corinthians 13:2", "Love Keeps Going"]),
 (12, "D", "What If I Pray and Look Foolish?",
  "an ordinary Christian who would like to pray for a sick friend or neighbour but is afraid of looking foolish if nothing happens",
  "that they see whose name is really on the line, and feel brave enough to ask",
  ["08"],
  ["Elijah on Mount Carmel (1 Kings 18), as the book tells it under “Fire on Carmel”.",
   "Psalm 25:2-3 and Romans 10:11, read aloud: those who hope in Him will never be put to shame.",
   "“What If Nothing Happens?”: how to stay kind, and keep going."],
  "08", "Psalm 25:2–3", "fire",
  "On Mount Carmel, Elijah prayed in front of everyone. For anyone afraid of looking foolish if they pray for someone.",
  ["Fire on Carmel", "Psalm 25:2", "Romans 10:11", "What If Nothing Happens"]),
 (13, "E", "How Long Do I Keep Asking?",
  "someone who has prayed for a long time, for themselves or for someone they love, and is wondering whether to stop asking",
  "that they find the courage to keep asking, without pressure and without blame",
  ["13"],
  ["Elijah praying for rain and sending his servant to look towards the sea seven times (1 Kings 18:43-44), as the book tells it.",
   "The widow who kept asking, and Luke 18:1: pray at all times and do not lose heart. Read it aloud.",
   "Hebrews 10:35-36, read aloud, and “Do Not Throw Away Your Confidence”."],
  "13", "Hebrews 10:35–36", "cloud",
  "Elijah prayed for rain and sent his servant to look towards the sea seven times. For anyone wondering whether to keep asking.",
  ["Elijah", "Luke 18:1", "Hebrews 10:35", "Do Not Throw Away Your Confidence"]),
 (14, "F", "What Did Jesus Carry for Us?",
  "a Christian who knows Jesus died for their sins but has never thought that His suffering had anything to do with sickness",
  "that they see what the Bible says Jesus carried, and why the book can say, “By His stripes we are healed”",
  ["02"],
  ["Isaiah 53:4-5 and 1 Peter 2:24, read aloud, and what the book says under “He Carried Our Sickness” and “Stripes”.",
   "The paralysed man whose friends lowered him through the roof (Mark 2), as the book tells it.",
   "“Never a Weapon”: this truth must never be used to blame anyone who is still sick."],
  "02", "1 Peter 2:24", "cross",
  "What the Bible says Jesus carried to the cross, the friends who lowered a man through a roof, and why this truth is never a weapon.",
  ["Isaiah 53", "1 Peter 2:24", "He Carried Our Sickness", "roof", "Never a Weapon"]),
 (15, "G", "Why Did Jesus Heal?",
  "a pastor or prayer leader who wants the people they lead to pray for the sick for the right reason",
  "that they see compassion moved Jesus, and that they ask Him for His heart first",
  ["10"],
  ["The widow of Nain: nobody asked, and Jesus saw her and had compassion (Luke 7:11-15), as the book tells it under “Nobody Asked”.",
   "Matthew 14:14, read aloud, and “Jesus Saw, and Jesus Felt”.",
   "“Without Love, Nothing” and “Ask for His Heart”."],
  "10", "Luke 7:13", "heart",
  "Nobody asked Jesus for anything at the gate of Nain. He saw a widow, and He had compassion on her.",
  ["Nain", "Nobody Asked", "Matthew 14:14", "Jesus Saw, and Jesus Felt", "Without Love, Nothing", "Ask for His Heart"]),
 (16, "H", "Why Do Christians Pray “in Jesus’ Name”?",
  "someone who has heard Christians end their prayers with “in Jesus' name” and wonders what it means, and whether it is a habit or a magic phrase",
  "that they understand that the name of Jesus means Jesus Himself, alive and near",
  ["09"],
  ["Aeneas at Lydda, to whom Peter said, “Jesus Christ heals you!” (Acts 9:32-35), as the book tells it.",
   "John 14:13-14, read aloud, and “The Name Above Every Name”.",
   "The seven sons of Sceva: the difference between using a name and knowing the Person."],
  "09", "John 14:13–14", "crown",
  "Peter said to a man named Aeneas, “Jesus Christ heals you!” What it means to pray in the name of Jesus.",
  ["Aeneas", "John 14:13", "The Name Above Every Name", "Sceva"]),
 (17, "A", "Can I Reach Out to Jesus Myself?",
  "someone who is sick and has always asked other people to pray for them, and wonders whether they can come to Jesus themselves",
  "that they know they can reach out to Jesus themselves, today",
  ["06"],
  ["The woman who had been ill for twelve years and pressed through the crowd to touch Jesus' cloak (Mark 5:25-34), as the book tells it under “She Kept Saying”.",
   "Mark 5:28, read aloud: what she kept saying to herself.",
   "“Expectation Is Not Pressure”: expecting God to act is not a test you can fail."],
  "06", "Mark 5:28", "cloak",
  "A woman who had been ill for twelve years pressed through the crowd to touch Jesus' cloak. For anyone who wonders whether they can come to Jesus themselves.",
  ["She Kept Saying", "Mark 5:28", "Expectation Is Not Pressure"]),
 (18, "B", "Can I Keep Asking for My Child?",
  "a mother or father who has asked Jesus again and again for their child, and wonders whether they should stop",
  "that they feel free to keep asking, like the mother in the Gospel",
  ["13"],
  ["The Canaanite mother who kept asking Jesus for her daughter, and His answer, “your faith is great” (Matthew 15:28), as the book tells it.",
   "“Keep Asking”, and Luke 18:1, read aloud.",
   "“Never Blame the Sick”: a child who is still sick is never to blame, and neither is the parent."],
  "13", "Matthew 15:28", "kneel",
  "A mother kept asking Jesus for her daughter, and He said, “Your faith is great.” For every parent who has asked again and again.",
  ["Canaanite", "Matthew 15:28", "Keep Asking", "Luke 18:1", "Never Blame the Sick"]),
 (19, "C", "What Do We Do After We Pray?",
  "someone who has just prayed with a person they love and is not sure what to do next",
  "that they know the gentle next steps, and that any change is to be confirmed by a doctor",
  ["11"],
  ["Steps 6 to 9 of the model in the book: check, pray again, give thanks and point to Jesus, go and show yourself.",
   "The second touch at Bethsaida (Mark 8:23-25): Jesus Himself prayed twice.",
   "The ten lepers, and the one who came back to give thanks (Luke 17:14-16). Read it aloud."],
  "11", "Luke 17:14–16", "ten",
  "Ten men with leprosy went on their way as Jesus told them, and one came back to give thanks. What to do after you have prayed.",
  ["Pray Again", "Give Thanks", "Mark 8:23", "Luke 17:14"]),
 (20, "D", "What Do I Actually Say When I Pray?",
  "an ordinary Christian who is willing to pray for a sick friend but does not know what words to use",
  "that they could pray a short, simple prayer tomorrow: ask the Father, then speak in Jesus' name",
  ["09"],
  ["Peter and Tabitha: he knelt and prayed, then turned and said, “Tabitha, get up!” (Acts 9:40), as the book tells it under “Pray, Then Speak”.",
   "“Asking the Father” and “Speaking to the Sickness”: a short, calm prayer, never a performance.",
   "“All the Glory to Jesus”."],
  "09", "Acts 9:40", "needle",
  "Peter knelt and prayed, then said, “Tabitha, get up!” The simple words of a prayer for someone who is sick.",
  ["Tabitha", "Pray, Then Speak", "Acts 9:40", "Asking the Father", "Speaking to the Sickness", "All the Glory to Jesus"]),
 (21, "E", "What Do I Do with My Doubts?",
  "someone who believes in Jesus but, after waiting a long time, finds doubts creeping in, and feels guilty about them",
  "that they see Jesus reaches out His hand to people who doubt, and that they can keep their eyes on Him",
  ["07"],
  ["Peter walking on the water, and how Jesus immediately reached out His hand and took hold of him (Matthew 14:28-31), as the book tells it.",
   "“Eyes on Jesus” and “Feed Your Faith”, with Romans 10:17, read aloud.",
   "“What Faith Is Not”: faith is not pretending, and it is not pressure."],
  "07", "Matthew 14:28–31", "rock",
  "Peter walked on the water, saw the wind and began to sink, and Jesus reached out His hand. For anyone whose doubts have crept in while they wait.",
  ["Matthew 14:28", "Eyes on Jesus", "Feed Your Faith", "Romans 10:17", "What Faith Is Not"]),
 (22, "F", "Is Jesus Still the Same Today?",
  "a Christian who reads about Jesus healing people in the Bible and wonders whether He would do the same today",
  "that they see Jesus has not changed, and that His answer is still “I am willing”",
  ["01"],
  ["The man with leprosy who asked Jesus whether He was willing, and how Jesus touched him and said, “I am willing” (Mark 1:40-42), as the book tells it.",
   "Hebrews 13:8, read aloud, and “He Has Not Changed”.",
   "“Show Us the Father”: anyone who has seen Jesus has seen the Father (John 14:9)."],
  "01", "Mark 1:41", "hand",
  "A man with leprosy asked Jesus whether He was willing. Jesus touched him and said, “I am willing.” Is He the same today?",
  ["Mark 1:41", "I Am Willing", "Hebrews 13:8", "He Has Not Changed", "Show Us the Father", "John 14:9"]),
 (23, "G", "Who Gets the Glory?",
  "a pastor or prayer leader who wants every answered prayer in their church to point people to Jesus, not to a person or a ministry",
  "that they know how to give Jesus all the glory and point people to Him",
  ["06", "09"],
  ["Peter and John at the temple gate called Beautiful: “Look at us!” and “What I have I give you” (Acts 3:1-8), as the book tells it.",
   "What Peter said to the crowd afterwards, Acts 3:16, read aloud, and “All the Glory to Jesus”.",
   "How to tell someone one sentence about who Jesus is after praying for them."],
  "09", "Acts 3:16", "gate",
  "Peter and John at the temple gate called Beautiful, and what Peter told the crowd afterwards. Why every answered prayer points to Jesus.",
  ["Look at Us", "What I Have I Give You", "Acts 3:16", "All the Glory to Jesus"]),
 (24, "H", "Where Do I Begin?",
  "someone new to faith, or coming back to God, who has read about Jesus healing people and wants to know where to begin",
  "that they have one sentence to hold on to: find what God has said, ask Him to do what He said, and expect Him to do it",
  ["00", "15"],
  ["The key to prayer, in the book's words: “Find what God has said in His Word, ask Him to do what He said, and expect Him to do it.” Explain each part simply.",
   "“Do Your Homework on God”: God has never broken His word (Numbers 23:19), and 2 Corinthians 1:20, read aloud.",
   "One promise from “Healing Scriptures to Stand On”: 1 John 5:14-15, read aloud."],
  "00", "2 Corinthians 1:20", "key",
  "One sentence to hold on to: find what God has said in His Word, ask Him to do what He said, and expect Him to do it.",
  ["Find what God has said", "Do Your Homework on God", "Numbers 23:19", "CORINTHIANS 1:20", "1 John 5:14"]),
]

# Said the same way in every episode. Kept short and positive: what to do, not what to avoid.
TEMPLATE = """Who is listening: {listener}. Their question is: “{title}”

This episode is for that one person. The aim: {outcome}. Answer from Graham Marsland's book How to Pray for the Sick and Expect a Miracle, and from the Bible.

Build the conversation around three things:
1. {p1}
2. {p2}
3. {p3}

Begin with one sentence saying that you are two voices made with artificial intelligence, talking through Graham Marsland's book How to Pray for the Sick and Expect a Miracle. Then ask the question.

How to talk: like two warm friends at a kitchen table with someone who is hurting. Plain everyday words and short sentences. Explain any Bible word the first time. Speak to the listener as “you”. Call what you are reading “the book” or “Graham's book”. Use pictures from the Bible and from ordinary family life. Tell only the stories that are in the book, the way the book tells them; you have no stories of your own.

Keep it gentle and true: promise no healing and no timing; never suggest that anyone is sick because of weak faith or sin; say that any healing should be checked by a doctor, and encourage the listener to keep seeing their doctor.

End like this: give the listener one simple thing to do this week. Then pray the book's prayer that begins “{prayer}” slowly, so the listener can pray along{prayer_note}. Finish with: “Jesus is the healer.”"""


def build():
    eps = []
    for n, lens, title, listener, outcome, parts, (p1, p2, p3), pk, ref, picture, line, checks in E:
        note = (", and say first that it was written for a reader holding the book and is for the listener too"
                if pk == "00" else "")
        prompt = TEMPLATE.format(listener=listener, title=title.replace("“", "'").replace("”", "'").replace("’", "'"),
                                 outcome=outcome, p1=p1, p2=p2, p3=p3, prayer=PRAYER[pk], prayer_note=note)
        eps.append({"number": n, "lens": lens, "lensTitle": LENSES[lens], "title": title,
                    "sources": [PART_NAME[k] for k in parts], "partKeys": parts,
                    "scripture": ref, "picture": picture, "description": line,
                    "prompt": prompt, "promptLength": len(prompt), "checks": checks})
    return {"lenses": LENSES, "episodes": eps}


if __name__ == "__main__":
    data = build()
    out = pathlib.Path(__file__).with_name("lens_episodes.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    lens_of = [e["lens"] for e in data["episodes"]]
    assert all(lens_of[i] != lens_of[i + 1] for i in range(len(lens_of) - 1)), "two neighbours share a lens"
    assert sorted(lens_of) == sorted(list("ABCDEFGH") * 3)
    assert len({e["picture"] for e in data["episodes"]}) == 24, "pictures are not unique"
    print(json.dumps({"episodes": len(data["episodes"]), "longest_prompt": max(e["promptLength"] for e in data["episodes"]),
                      "shortest_prompt": min(e["promptLength"] for e in data["episodes"])}))
