#pragma once
#include <array>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include "utils.h"

template<std::size_t N>
class CrabCups {
	template<std::size_t M>
	friend std::ostream& operator<< (std::ostream&, const CrabCups<M>&);
private:
	const unsigned int swapped = 3;
	unsigned int moves = 0;
	std::array<unsigned, N> data_;

public:
	explicit constexpr CrabCups(std::array<unsigned, N> data)
		: data_(data)
	{}

public:
	void show() const
	{
		spdlog::info("cups: {}", *this);
	}
};

template<std::size_t M, std::size_t N>
constexpr CrabCups<M> make_crabcups(const char(&data)[N + 1]) 
{ 
	return CrabCups<M>(utils::combine<N, M>(data));
}

template<std::size_t N> 
inline std::ostream& operator<<(std::ostream& os, const CrabCups<N>& cc)
{
	for (auto& i : cc.data_)
		os << " " << i << " ";
	return os;
}
