#include <algorithm>
#include <array>
#include <compare>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <memory>
#include <vector>

struct Coord {
  int32_t x, y;

  constexpr Coord operator+(const Coord &other) const {
    return {x + other.x, y + other.y};
  }

  constexpr Coord operator-(const Coord &other) const {
    return {x - other.x, y - other.y};
  }

  constexpr auto operator<=>(const Coord &) const = default;

  constexpr Coord min(const Coord &other) const {
    return {std::min(x, other.x), std::min(y, other.y)};
  }

  constexpr Coord max(const Coord &other) const {
    return {std::max(x, other.x), std::max(y, other.y)};
  }

  constexpr Coord normalize() const {
    return {x ? x / std::abs(x) : 0, y ? y / std::abs(y) : 0};
  }
};

#define at(a, p, n) a[p.y * n + p.x]

int main() {
  const int level = 2;
  const int N = 200;
  const int M = 1000;

  auto m = std::make_unique<char[]>(N * M);
  std::fill(m.get(), m.get() + N * M, '.');

  std::ifstream file("input.txt");
  if (!file) {
    return 1;
  }
  std::string line;
  int32_t max_y{};
  while (true) {
    int32_t x, y;
    Coord cur, prev;
    bool p{false};
    bool last{false};
    char c;
    std::getline(file, line);
    if (!file) {
      break;
    }
    std::stringstream stream(line);
    while (true) {
      stream >> x >> c >> y;
      max_y = std::max(max_y, y);
      cur = {x, y};
      stream >> std::noskipws >> c >> c >> c >> c;
      if (!stream) {
        last = true;
      }
      if (p) {
        const auto vel = (cur - prev).normalize();
        auto pos = prev;
        while (true) {
          at(m, pos, M) = '#';
          // std::cout << pos.x << " " << pos.y << std::endl;
          if (pos == cur) {
            break;
          }
          pos = pos + vel;
        }
      } else {
        p = true;
      }
      prev = cur;
      if (last) {
        break;
      }
    }
  }

  int ans{};
  Coord pos{};
  Coord source{500, 0};
  std::array<Coord, 3> checks{Coord{0, 1}, Coord{-1, 1}, Coord{1, 1}};
  bool pos_ready{false};
  bool ready{false};
  // TODO
  int standing_y{max_y + 2};

  while (true) {
    if (ready) {
      break;
    }

    at(m, source, M) = '+';
    if (!pos_ready) {
      ans += 1;
      pos = source;
      pos_ready = true;
      at(m, source, M) = 'o';
      continue;
    }

    bool none = true;
    for (const auto check_vel : checks) {
      const auto check_pos = pos + check_vel;

      if (level == 1 && check_pos.y >= 200) {
        ready = true;
        ans--;
        none = false;
        break;
      }

      if (level == 2) {
        if (check_pos.y == standing_y) {
          at(m, check_pos, M) = '#';
        }
      }

      if (at(m, check_pos, M) == '.') {
        at(m, pos, M) = '.';
        at(m, check_pos, M) = 'o';
        pos = check_pos;
        none = false;
        break;
      }
    }
    if (none) {
      pos_ready = false;
      if (level == 2 && pos == source) {
        break;
      }
    }
  }
  std::cout << ans << std::endl;
}