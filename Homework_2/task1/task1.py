# Задание 1. Создайте реализацию паттерна Command.
# Протестируйте работу созданного класса.

print("Задание №1 — Паттерн Command (Медиаплеер)")
print("-" * 45)


# ===== Интерфейс команды =====
class MediaCommand:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


# ===== Получатель =====
class MediaPlayer:
    @staticmethod
    def play():
        print("▶ Воспроизведение начато")

    @staticmethod
    def pause():
        print("⏸ Воспроизведение приостановлено")

    @staticmethod
    def stop():
        print("⏹ Воспроизведение остановлено")


# ===== Конкретные команды =====
class PlayCommand(MediaCommand):
    def __init__(self, player: MediaPlayer):
        self.player = player

    def execute(self):
        self.player.play()

    def undo(self):
        self.player.pause()


class PauseCommand(MediaCommand):
    def __init__(self, player: MediaPlayer):
        self.player = player

    def execute(self):
        self.player.pause()

    def undo(self):
        self.player.play()


class StopCommand(MediaCommand):
    def __init__(self, player: MediaPlayer):
        self.player = player

    def execute(self):
        self.player.stop()

    def undo(self):
        self.player.play()


# ===== Инициатор =====
class ControlPanel:
    def __init__(self):
        self.history = []

    def press(self, command: MediaCommand):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if self.history:
            last = self.history.pop()
            last.undo()


# ===== Тестирование =====
def test_media_player():
    player = MediaPlayer()
    panel = ControlPanel()

    panel.press(PlayCommand(player))
    panel.press(PauseCommand(player))
    panel.press(StopCommand(player))

    print("↩ Отмена последней команды")
    panel.undo_last()

    print("✅ Тест Command завершён\n")


if __name__ == "__main__":
    test_media_player()
