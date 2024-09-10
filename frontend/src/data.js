// List of supported services
export const musicServices = [
  {
    name: "Spotify",
    domain: "open.spotify.com",
    urlPath: "playlist",
    color: "#1ED760",
  },
  // Soundcloud and yandex music will be supported later
];

export const analysisPhases = [
  {
    max: 20,
    phrases: [
      "Your playlist is just getting started! (๑•̀ㅂ•́)و✧",
      "Everyone starts somewhere! (•‿•)",
      "You're warming up — keep going! (｡♥‿♥｡)",
      "You've got potential here! (๑˃ᴗ˂)ﻭ",
      "Music journey begins with a step! (＾▽＾)",
    ],
    gradient: "linear(90deg, red.400, red.600)",
  },
  {
    max: 40,
    phrases: [
      "Not bad, you're on the right track! (｡•̀ᴗ-)✧",
      "This playlist is getting interesting! (☆ω☆)",
      "You're finding your rhythm! (｡♥‿♥｡)",
      "There's something cool here! (≧◡≦)",
      "Good vibes, keep it up! (＾▽＾)",
    ],
    gradient: "linear(50deg, orange.400, orange.600)",
  },
  {
    max: 60,
    phrases: [
      "You're mixing it up nicely! (๑>ᴗ<๑)",
      "Great balance of tunes! (◕‿◕)",
      "Your playlist is coming together! (•̀ᴗ•́)و",
      "Both familiar and fresh — nice job! (｡♥‿♥｡)",
      "You're hitting a sweet spot! (๑˃ᴗ˂)ﻭ",
    ],
    gradient: "linear(10deg, yellow.400, yellow.600)",
  },
  {
    max: 80,
    phrases: [
      "Wow, you're a real trendsetter! (⌒ω⌒)",
      "This playlist is lit! (☆ω☆)",
      "You've got a great ear for music! (＾▽＾)",
      "This is the playlist of a pro! (๑•̀ㅂ•́)و✧",
      "You're on fire with these tracks! (¬‿¬)",
    ],
    gradient: "linear(20deg, green.400, green.600)",
  },
  {
    max: 100,
    phrases: [
      "This playlist is pure gold! (✧ω✧)",
      "You're a music genius! (⌐■_■)",
      "Your taste is off the charts! (♥‿♥)",
      "What a unique selection! (＾▽＾)",
      "You've created a masterpiece! (๑•̀ㅂ•́)و✧",
    ],
    gradient: "linear(40deg, cyan.400, blue.400)",
  },
];

export const tracksCountPhrases = [
  {
    max: 5,
    phrases: [
      "Your playlist has a cozy number of tracks! (◠‿◠✿)",
      "Look at that, just a few tracks! Time to get the party started! ヾ(＾-＾)ノ",
      "Ooh la la, that's a nice little playlist you've got there! (≧◡≦)",
    ],
  },
  {
    max: 10,
    phrases: [
      "Wow, your playlist is really getting groovy! ヽ(✿ﾟ▽ﾟ)ノ",
      "Nifty, your collection is growing nicely! (◕‿◕)✧",
      "Cool beans, time to crank up the volume! ᕕ( ᐛ )ᕗ",
    ],
  },
  {
    max: 20,
    phrases: [
      "Niiice, you're building up quite the collection! (☞ﾟ∀ﾟ)☞",
      "Impressive, your music game is on point! ヾ(◍°∇°◍)ﾉ",
      "Rockin', you're quite the audiophile, aren't you? ୧(＾ 〰 ＾)୨",
    ],
  },
  {
    max: 40,
    phrases: [
      "Incredible, you must be a music maven! (◠‿◠✨)",
      "Whoa, your playlist is out of this world! (⊙_⊙)",
      "Holy moly, you're a true music connoisseur! (≧▽≦)",
    ],
  },
  {
    max: 80,
    phrases: [
      "Woah, you're a music marathon runner! ᕙ(⇀‸↼‶)ᕗ",
      "Incredible, you must listen to music all day long! (◍•ᴗ•◍)❤",
      "Your playlist is massive, you're the soundtrack of our lives! ٩(◕‿◕)۶",
    ],
  },
  {
    max: 100,
    phrases: [
      "Whoa, you must have the ultimate playlist! ୧(＾ 〰 ＾)୨",
      "Holy cow, you're a true audiophile and then some! (⊙_☉)",
      "Unbelievable, your music collection is out of this world! ᕦ(ò_óˇ)ᕤ",
    ],
  },
  {
    max: 200,
    phrases: [
      "Jaw-dropping, you must have the mother of all playlists! ୧(＾ 〰 ＾)୨",
      "Inconceivable, you're a musical legend in the making! (⊙_⊙)",
      "Unfathomable, your music knowledge is off the charts! ᕦ(ò_óˇ)ᕤ",
    ],
  },
  {
    max: 500,
    phrases: [
      "Mind-blowing, you must be the Spotify CEO in disguise! (─‿‿─)",
      "Unreal, you're a musical savant, plain and simple! (⊙_☉)",
      "Inconceivable, your playlist could rival the Billboard Top 100! (☆▽☆)",
    ],
  },
  {
    // Current spotify limit for tracks in playlist is 10k (I don't think anybody can get this number)
    max: 10000,
    phrases: [
      "Transcendent, your music collection is beyond comprehension! (￣▽￣*)ゞ",
      "Legendary, your playlist is the stuff of musical lore! (＾▽＾)",
      "Godlike, your musical domain knows no bounds! ᕙ(⇀‸↼‶)ᕗ",
    ],
  },
];
