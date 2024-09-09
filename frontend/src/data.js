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
      "Oh, this is so mainstream!",
      "Your playlist is like déjà vu — I've heard this before!",
      "Well, it's kinda...",
    ],
    color: "#FF0000",
  },
  {
    max: 40,
    phrases: ["Well, it's could be worse", "It's like turning on the radio during rush hour"],
    color: "#FF6347",
  },
  {
    max: 60,
    phrases: ["A mix of old and new", "You've got both classics and trends here"],
    color: "#FFD700",
  },
  {
    max: 80,
    phrases: [
      "A playlist for true connoisseurs!",
      "With this playlist, you're definitely on trend",
      "Cool, but not 100%",
    ],
    color: "#32CD32",
  },
  {
    max: 100,
    phrases: [
      "Wow! A playlist like a rare butterfly!",
      "As unique as a fingerprint!",
      "Now you're definitely not a normal guy!",
    ],
    color: "#00FF7F",
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
