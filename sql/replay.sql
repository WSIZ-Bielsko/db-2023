CREATE TABLE channel(
    channel_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL CHECK(username ~ '^[ -~]{1,50}$')
);

CREATE TABLE video(
    video_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    title TEXT NOT NULL CHECK(title ~ '^[ -~]{1,50}$'),
    owner UUID NOT NULL REFERENCES channel(channel_id),
    filename TEXT NOT NULL CHECK(filename ~ '^[ -~]{1,255}$'),
    description TEXT NOT NULL CHECK(title ~ '^[ -~]{1,100}$'),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
);

CREATE TABLE video_likes(
    video_id UUID NOT NULL REFERENCES video(video_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id),
    is_like BOOLEAN NOT NULL
);

CREATE TABLE video_views(
    video_id UUID NOT NULL REFERENCES video(video_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id)
);

CREATE TABLE video_flags(
    video_id UUID NOT NULL REFERENCES video(video_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id)
);

CREATE TABLE comment(
    comment_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    author UUID NOT NULL REFERENCES channel(channel_id),
    content TEXT NOT NULL CHECK(content ~ '^[ -~]{1,}$' and length(content) < 500),
    video_id UUID NOT NULL REFERENCES video(video_id),
    parent_comment UUID REFERENCES comment(comment_id) CHECK(parent_comment != comment_id),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
);

CREATE TABLE comment_likes(
    comment_id UUID NOT NULL REFERENCES comment(comment_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id),
    is_like BOOLEAN NOT NULL
);

CREATE TABLE playlist(
    playlist_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    playlist_name TEXT NOT NULL CHECK(playlist_name ~ '^[ -~]{1,50}$'),
    playlist_owner UUID NOT NULL REFERENCES channel(channel_id),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
);

CREATE TABLE playlist_video(
    playlist_id UUID NOT NULL REFERENCES playlist(playlist_id),
    video_id UUID NOT NULL REFERENCES video(video_id)
);

CREATE TABLE playlist_views(
    playlist_id UUID NOT NULL REFERENCES playlist(playlist_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id)
);