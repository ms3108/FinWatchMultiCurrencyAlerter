package com.example.snarkyoverlay;

import java.util.Random;

public class SnarkGenerator {

    private static final String[] GENERIC_SNARKS = {
            "Is this really the best use of your time?",
            "Wow, fascinating content... not.",
            "I'm bored. Are you bored?",
            "You click too much.",
            "Scrolling into the void, are we?",
            "Do you ever go outside?",
            "This app is judging you."
    };

    private static final String[] SOCIAL_MEDIA_SNARKS = {
            "Another cat video? Really?",
            "Comparing your life to others again?",
            "Doomscrolling is bad for your health.",
            "None of these people care about you."
    };

    private static final String[] SETTINGS_SNARKS = {
            "Changing settings won't fix your life.",
            "What did you break this time?",
            "Searching for a 'dark mode' for your soul?"
    };

    private static final String[] PRODUCTIVITY_SNARKS = {
            "Pretending to work?",
            "You have 50 unread emails. Just delete them.",
            "This meeting could have been an email."
    };

    public static String getSnark(String screenText) {
        String lowerText = screenText.toLowerCase();
        Random random = new Random();

        if (lowerText.contains("instagram") || lowerText.contains("twitter") || lowerText.contains("facebook") || lowerText.contains("tiktok")) {
            return SOCIAL_MEDIA_SNARKS[random.nextInt(SOCIAL_MEDIA_SNARKS.length)];
        } else if (lowerText.contains("settings") || lowerText.contains("configuration")) {
            return SETTINGS_SNARKS[random.nextInt(SETTINGS_SNARKS.length)];
        } else if (lowerText.contains("mail") || lowerText.contains("docs") || lowerText.contains("sheet")) {
            return PRODUCTIVITY_SNARKS[random.nextInt(PRODUCTIVITY_SNARKS.length)];
        }

        return GENERIC_SNARKS[random.nextInt(GENERIC_SNARKS.length)];
    }
}
