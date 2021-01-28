#include <spdlog/spdlog.h>
#include <spdlog/stopwatch.h>

#include "CrabCupsFast.h"

int main() {

	spdlog::set_level(spdlog::level::info);
	{
		spdlog::debug("Initializing...");
		spdlog::stopwatch sw;
		auto cc = CrabCups("871369452");
		spdlog::debug("Initialized in {:.3}s", sw);
		spdlog::debug("Starting...");
		spdlog::stopwatch sw2;
		for (unsigned i = 0; i < 100; i++)
			cc.move_detailed();
		cc.set_formatted(false);
		spdlog::debug("Completed in {:.3}s", sw2);
		spdlog::info("Part 1: {}", cc);
	}

	spdlog::set_level(spdlog::level::debug);
	{
		spdlog::debug("Initializing...");
		spdlog::stopwatch sw;
		auto cc = CrabCups<9, 1000000>("871369452");
		spdlog::debug("Initialized in {:.3}s", sw);
		spdlog::debug("Starting...");
		spdlog::stopwatch sw2;
		for (unsigned i = 0; i < 10000000; i++)
			cc.move();
		spdlog::debug("Completed in {:.3}s", sw2);
		std::size_t first = cc.follow(1, 1);
		std::size_t second = cc.follow(1, 2);
		spdlog::info("Part 2: {} * {} = {}", first, second, first * second);
	}

}
