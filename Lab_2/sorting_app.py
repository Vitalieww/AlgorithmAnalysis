import pygame
import random
import threading
from algorithms import quicksort, mergesort, heapsort, introsort

# ── Constants ────────────────────────────────────────────────────────────────
W, H     = 1280, 720
PANEL_W  = 260
FPS      = 60
ARRAY_SIZE = 60

BACKGROUND   = (15, 15, 25)
BAR_DEFAULT  = (70, 130, 220)
BAR_ACTIVE   = (255, 80,  80)
BAR_SORTED   = (80, 220, 120)
TEXT_COLOR   = (220, 220, 220)
PANEL_COLOR  = (25, 25, 40)
BTN_COLOR    = (50,  80, 160)
BTN_HOVER    = (80, 120, 210)
BTN_ACTIVE   = (30, 180, 100)
INPUT_BG     = (30, 30, 50)
INPUT_ACTIVE_BG = (45, 45, 70)
INPUT_BORDER = (100, 130, 200)
ERROR_COLOR  = (255, 80, 80)
LABEL_COLOR  = (140, 150, 180)
SEP_COLOR    = (60, 60, 100)

ALGORITHMS = {
    "QuickSort": quicksort,
    "MergeSort": mergesort,
    "HeapSort":  heapsort,
    "IntroSort": introsort,
}
INPUT_TYPES = ["random", "sorted", "reverse", "almost_sorted", "duplicates"]
SPEEDS      = {"Slow": 0.08, "Normal": 0.03, "Fast": 0.008, "Turbo": 0.001}


# ── Helpers ───────────────────────────────────────────────────────────────────
def generate_input(size, input_type):
    if input_type == "sorted":
        return list(range(1, size + 1))
    elif input_type == "reverse":
        return list(range(size, 0, -1))
    elif input_type == "almost_sorted":
        arr = list(range(1, size + 1))
        for _ in range(max(1, size // 10)):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif input_type == "duplicates":
        return [random.randint(1, 10) for _ in range(size)]
    return [random.randint(1, 100) for _ in range(size)]


# ── TrackedList ───────────────────────────────────────────────────────────────
class TrackedList(list):
    def __init__(self, data, on_write):
        super().__init__(data)
        self._on_write = on_write

    def __setitem__(self, idx, val):
        super().__setitem__(idx, val)
        self._on_write(list(self), [idx])


# ── Button ────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, font):
        self.rect     = pygame.Rect(rect)
        self.label    = label
        self.font     = font
        self.selected = False

    def draw(self, surf, mouse_pos):
        if self.selected:
            color = BTN_ACTIVE
        elif self.rect.collidepoint(mouse_pos):
            color = BTN_HOVER
        else:
            color = BTN_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=5)
        pygame.draw.rect(surf, SEP_COLOR, self.rect, 1, border_radius=5)
        txt = self.font.render(self.label, True, TEXT_COLOR)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ── TextInput ─────────────────────────────────────────────────────────────────
class TextInput:
    ALLOWED = set("0123456789, -")

    def __init__(self, rect, font, placeholder="e.g. 5, 3, 8, 1, 9"):
        self.rect        = pygame.Rect(rect)
        self.font        = font
        self.placeholder = placeholder
        self.text        = ""
        self.active      = False
        self.error       = ""
        self._blink_vis  = True
        self._blink_t    = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                self.error = ""
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.error = ""
            elif event.key == pygame.K_DELETE:
                self.text = ""
                self.error = ""
            elif event.unicode in self.ALLOWED:
                self.text += event.unicode
                self.error = ""

    def parse(self):
        raw = self.text.strip()
        if not raw:
            return None, "Input is empty"
        try:
            values = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            return None, "Invalid number found"
        if len(values) < 2:
            return None, "Need at least 2 numbers"
        if len(values) > 150:
            return None, "Max 150 elements"
        return values, ""

    def update(self, dt_ms):
        self._blink_t += dt_ms
        if self._blink_t >= 500:
            self._blink_vis = not self._blink_vis
            self._blink_t   = 0

    def draw(self, surf):
        bg = INPUT_ACTIVE_BG if self.active else INPUT_BG
        pygame.draw.rect(surf, bg, self.rect, border_radius=4)
        border = (180, 80, 80) if self.error else INPUT_BORDER
        pygame.draw.rect(surf, border, self.rect, 1, border_radius=4)

        pad     = 4
        inner_w = self.rect.width - pad * 2
        display = (self.text + ("|" if self.active and self._blink_vis else "")) if self.text else ""

        if display:
            lines = self._wrap(display, inner_w)
            for li, line in enumerate(lines[-4:]):
                ts = self.font.render(line, True, TEXT_COLOR)
                surf.blit(ts, (self.rect.x + pad, self.rect.y + pad + li * (self.font.get_height() + 1)))
        else:
            ph_text = self.placeholder + ("|" if self.active and self._blink_vis else "")
            ts = self.font.render(ph_text, True, (80, 90, 110))
            surf.blit(ts, (self.rect.x + pad, self.rect.y + pad))

        if self.error:
            es = self.font.render(self.error, True, ERROR_COLOR)
            surf.blit(es, (self.rect.x, self.rect.bottom + 2))

    def _wrap(self, text, max_width):
        lines, current = [], ""
        for ch in text:
            if self.font.size(current + ch)[0] <= max_width:
                current += ch
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
        return lines


# ── SortingApp ────────────────────────────────────────────────────────────────
class SortingApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Sorting Visualizer")
        self.clock  = pygame.time.Clock()

        self.font_sm  = pygame.font.SysFont("Consolas", 13)
        self.font_med = pygame.font.SysFont("Consolas", 14, bold=True)
        self.font_lg  = pygame.font.SysFont("Consolas", 18, bold=True)

        self.selected_alg   = "QuickSort"
        self.selected_input = "random"
        self.selected_speed = "Normal"
        self.array: list[int] = []
        self.highlights: list[int] = []
        self.sorted_flag = False
        self.running_sort = False
        self.swaps        = 0
        self.elapsed_ms   = 0
        self._sort_thread: threading.Thread | None = None
        self._stop_event  = threading.Event()
        self._accum       = 0.0
        self._steps: list  = []
        self._step_lock    = threading.Lock()

        self._build_ui()
        self._new_array()

    # ── layout constants ──────────────────────────────────────────────────────
    #  We divide the panel into rows manually so nothing overflows.
    #  All magic numbers come from this single _build_ui method.

    def _build_ui(self):
        x0 = 8
        bw = PANEL_W - 16
        bh = 24          # button height
        gap = 5          # gap between buttons
        y   = 38         # start below title

        def section(label, y):
            """Draw a section label (stored, not drawn here — just advance y)."""
            self._section_labels.append((label, y))
            return y + 16

        self._section_labels: list[tuple[str, int]] = []

        # ── Algorithm ─────────────────────────────────────────────────────────
        y = section("── Algorithm ──", y)
        self.alg_buttons: dict[str, Button] = {}
        for name in ALGORITHMS:
            self.alg_buttons[name] = Button((x0, y, bw, bh), name, self.font_sm)
            self.alg_buttons[name].selected = (name == self.selected_alg)
            y += bh + gap

        y += 4
        # ── Input type ────────────────────────────────────────────────────────
        y = section("── Input type ──", y)
        self.input_buttons: dict[str, Button] = {}
        for itype in INPUT_TYPES:
            self.input_buttons[itype] = Button((x0, y, bw, bh), itype, self.font_sm)
            self.input_buttons[itype].selected = (itype == self.selected_input)
            y += bh + gap

        y += 4
        # ── Speed ─────────────────────────────────────────────────────────────
        y = section("── Speed ──", y)
        self.speed_buttons: dict[str, Button] = {}
        for sp in SPEEDS:
            self.speed_buttons[sp] = Button((x0, y, bw, bh), sp, self.font_sm)
            self.speed_buttons[sp].selected = (sp == self.selected_speed)
            y += bh + gap

        y += 6
        # ── Action buttons ────────────────────────────────────────────────────
        self.btn_generate = Button((x0, y, bw, bh + 2), "Generate", self.font_med)
        y += bh + 2 + gap
        self.btn_sort     = Button((x0, y, bw, bh + 2), "Sort!", self.font_med)
        y += bh + 2 + gap
        self.btn_stop     = Button((x0, y, bw, bh + 2), "Stop", self.font_med)
        y += bh + 2 + gap + 6

        # ── Custom array ──────────────────────────────────────────────────────
        self._custom_sep_y = y
        y += 4
        self._custom_lbl_y = y
        y += 16
        input_h = self.font_sm.get_height() * 4 + 12   # 4 lines + padding
        self.text_input = TextInput(
            (x0, y, bw, input_h),
            self.font_sm,
            placeholder="e.g. 5, 3, 8, 1, 9",
        )
        y += input_h + 16   # +16 leaves room for error text
        self.btn_apply = Button((x0, y, bw, bh + 2), "Apply Array", self.font_med)
        y += bh + 2 + gap + 8

        # ── Stats (pinned near bottom, but stored as y for drawing) ───────────
        self._stats_y = max(y, H - 90)

    # ── Array helpers ─────────────────────────────────────────────────────────
    def _new_array(self):
        self._stop_sort()
        self.array       = generate_input(ARRAY_SIZE, self.selected_input)
        self.highlights  = []
        self.sorted_flag = False
        self.swaps = self.elapsed_ms = 0

    def _apply_custom_array(self):
        values, err = self.text_input.parse()
        if err:
            self.text_input.error = err
            return
        self._stop_sort()
        self.array       = values
        self.highlights  = []
        self.sorted_flag = False
        self.swaps = self.elapsed_ms = 0

    # ── Sort thread ───────────────────────────────────────────────────────────
    def _start_sort(self):
        if self.running_sort:
            return
        self._stop_event.clear()
        self.swaps = self.elapsed_ms = 0
        self.sorted_flag = False
        with self._step_lock:
            self._steps.clear()

        def on_write(snapshot, highlights):
            with self._step_lock:
                self._steps.append((snapshot, highlights))
            self.swaps += 1

        tracked          = TrackedList(list(self.array), on_write)
        self.running_sort = True
        self._start_time  = pygame.time.get_ticks()

        def worker():
            ALGORITHMS[self.selected_alg](tracked)
            with self._step_lock:
                self._steps.append(("DONE", []))

        self._sort_thread = threading.Thread(target=worker, daemon=True)
        self._sort_thread.start()

    def _stop_sort(self):
        self._stop_event.set()
        if self._sort_thread and self._sort_thread.is_alive():
            self._sort_thread.join(timeout=1.0)
        self.running_sort = False
        self._sort_thread = None
        with self._step_lock:
            self._steps.clear()

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _draw_panel(self, mouse_pos):
        pygame.draw.rect(self.screen, PANEL_COLOR, (0, 0, PANEL_W, H))
        pygame.draw.line(self.screen, SEP_COLOR, (PANEL_W, 0), (PANEL_W, H), 2)

        # Title
        self.screen.blit(
            self.font_lg.render("Sort Visualizer", True, TEXT_COLOR), (8, 10)
        )

        # Section labels
        for text, y in self._section_labels:
            self.screen.blit(self.font_sm.render(text, True, LABEL_COLOR), (8, y))

        for btn in self.alg_buttons.values():
            btn.draw(self.screen, mouse_pos)
        for btn in self.input_buttons.values():
            btn.draw(self.screen, mouse_pos)
        for btn in self.speed_buttons.values():
            btn.draw(self.screen, mouse_pos)

        self.btn_generate.draw(self.screen, mouse_pos)
        self.btn_sort.draw(self.screen, mouse_pos)
        self.btn_stop.draw(self.screen, mouse_pos)

        # Custom array section
        pygame.draw.line(self.screen, SEP_COLOR, (5, self._custom_sep_y), (PANEL_W - 5, self._custom_sep_y))
        self.screen.blit(
            self.font_sm.render("── Custom Array ──", True, LABEL_COLOR),
            (8, self._custom_lbl_y),
        )
        self.text_input.draw(self.screen)
        self.btn_apply.draw(self.screen, mouse_pos)

        # Stats
        pygame.draw.line(self.screen, SEP_COLOR, (5, self._stats_y - 6), (PANEL_W - 5, self._stats_y - 6))
        stats = [
            f"Alg  : {self.selected_alg}",
            f"Size : {len(self.array)}",
            f"Swaps: {self.swaps}",
            f"Time : {self.elapsed_ms / 1000:.2f}s",
        ]
        for i, line in enumerate(stats):
            self.screen.blit(
                self.font_sm.render(line, True, TEXT_COLOR),
                (8, self._stats_y + i * 16),
            )

    def _draw_bars(self):
        vis_x = PANEL_W + 8
        vis_w = W - vis_x - 8
        vis_h = H - 50
        vis_y = 30

        if not self.array:
            return

        max_val = max(self.array) or 1
        n   = len(self.array)
        bw  = max(1, (vis_w - n - 1) // n)
        total_bars_w = (bw + 1) * n
        start_x = vis_x + (vis_w - total_bars_w) // 2

        for i, val in enumerate(self.array):
            bar_h = max(1, int(val / max_val * vis_h))
            x = start_x + i * (bw + 1)
            y = vis_y + vis_h - bar_h
            if self.sorted_flag:
                color = BAR_SORTED
            elif i in self.highlights:
                color = BAR_ACTIVE
            else:
                color = BAR_DEFAULT
            pygame.draw.rect(self.screen, color, (x, y, bw, bar_h), border_radius=1)

        label = self.font_lg.render(
            f"{self.selected_alg}  |  {self.selected_input}  |  n={len(self.array)}",
            True, (180, 190, 220),
        )
        self.screen.blit(label, (vis_x + 8, 6))

    # ── Events ────────────────────────────────────────────────────────────────
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            self.text_input.handle_event(event)
            # Don't process button clicks while typing
            if self.text_input.active and event.type == pygame.KEYDOWN:
                continue

            for name, btn in self.alg_buttons.items():
                if btn.is_clicked(event):
                    self.selected_alg = name
                    for b in self.alg_buttons.values():
                        b.selected = False
                    btn.selected = True

            for itype, btn in self.input_buttons.items():
                if btn.is_clicked(event):
                    self.selected_input = itype
                    for b in self.input_buttons.values():
                        b.selected = False
                    btn.selected = True

            for sp, btn in self.speed_buttons.items():
                if btn.is_clicked(event):
                    self.selected_speed = sp
                    for b in self.speed_buttons.values():
                        b.selected = False
                    btn.selected = True

            if self.btn_generate.is_clicked(event):
                self._new_array()
            if self.btn_sort.is_clicked(event):
                self._start_sort()
            if self.btn_stop.is_clicked(event):
                self._stop_sort()
                self.highlights = []
            if self.btn_apply.is_clicked(event):
                self._apply_custom_array()

        return True

    # ── Step consumption ──────────────────────────────────────────────────────
    def _consume_steps(self, dt_ms):
        if not self.running_sort:
            return
        delay = SPEEDS[self.selected_speed]
        self._accum += dt_ms / 1000.0
        steps_this_frame = max(1, int(self._accum / delay)) if delay > 0 else 9999

        consumed = 0
        while consumed < steps_this_frame:
            with self._step_lock:
                if not self._steps:
                    break
                snapshot, highlights = self._steps.pop(0)
            if snapshot == "DONE":
                self.running_sort = False
                self.sorted_flag  = True
                self.highlights   = []
                self.elapsed_ms   = pygame.time.get_ticks() - self._start_time
                break
            self.array      = snapshot
            self.highlights = highlights
            consumed += 1

        if consumed:
            self._accum = 0.0

    # ── Main loop ─────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt        = self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()

            if not self._handle_events():
                break

            self._consume_steps(dt)
            self.text_input.update(dt)

            self.screen.fill(BACKGROUND)
            self._draw_bars()
            self._draw_panel(mouse_pos)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    SortingApp().run()