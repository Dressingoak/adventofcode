#include <spdlog/spdlog.h>

#include "CrabCups.h"

int main() {

	spdlog::set_level(spdlog::level::debug);

	constexpr auto cc = make_crabcups<100, 9>("871369452");
	cc.show();

}
