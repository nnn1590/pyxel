#ifndef PYXELCORE_SYSTEM_H_
#define PYXELCORE_SYSTEM_H_

#include "pyxelcore/constants.h"
#include "pyxelcore/profiler.h"
#include "pyxelcore/window.h"

namespace pyxelcore {

class Resource;
class Input;
class Graphics;
class Audio;

class System {
 public:
  System(int32_t width,
         int32_t height,
         const char* caption = DEFAULT_CAPTION,
         int32_t scale = DEFAULT_SCALE,
         const int32_t* palette_color = DEFAULT_PALETTE,
         int32_t fps = DEFAULT_FPS,
         int32_t border_width = DEFAULT_BORDER_WIDTH,
         int32_t border_color = DEFAULT_BORDER_COLOR);
  ~System();

  Resource* Resource() const { return resource_; }
  Input* Input() const { return input_; }
  Graphics* Graphics() const { return graphics_; }
  Audio* Audio() const { return audio_; }
  const int32_t* PaletteColor() const { return palette_color_; }

  int32_t Width() const { return window_->ScreenWidth(); }
  int32_t Height() const { return window_->ScreenHeight(); }
  int32_t FrameCount() const { return frame_count_; }

  void Run(void (*update)(), void (*draw)());
  void Quit();

 private:
  pyxelcore::Input* input_;
  pyxelcore::Resource* resource_;
  pyxelcore::Graphics* graphics_;
  pyxelcore::Audio* audio_;
  Window* window_;

  int32_t fps_;
  int32_t frame_count_;
  int32_t palette_color_[COLOR_COUNT];

  Profiler fps_profiler_;
  Profiler update_profiler_;
  Profiler draw_profiler_;
  bool is_performance_monitor_on;

  void UpdateFrame(void (*update)());
  void CheckSpecialInput();
  void DrawFrame(void (*draw)());
  void DrawPerformanceMonitor();
  void DrawMouseCursor();
};

}  // namespace pyxelcore

#endif  // PYXELCORE_SYSTEM_H_