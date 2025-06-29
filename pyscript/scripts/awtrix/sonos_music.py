import mqtt


@state_trigger("media_player.living_room")  # noqa F821
@state_trigger("media_player.living_room.media_title")  # noqa F821
def publish_song_details(**kwargs) -> None:
    if kwargs["value"] == "playing":
        mqtt.publish(
            topic="awtrix_2/notify",
            payload={
                "icon": "youtube",
                "text": (
                    f"{state.getattr('media_player.living_room')['media_artist']} - "  # noqa F821
                    + f"{state.getattr('media_player.living_room')['media_title']}"  # noqa F821
                ),
                "textCase": 2,
                "scrollSpeed": 80,
                "repeat": 3,
                "stack": False,
            },
        )
