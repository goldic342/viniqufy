// List of supported services
export const musicServices = [
  {
    name: "Spotify",
    playlistUrl: "https://open.spotify.com/playlist/",
    dataKey: "sptfy",
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
