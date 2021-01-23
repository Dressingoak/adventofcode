#pragma once
#include <vector>
#include <iterator>
#include <numeric>
#include <string_view>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

template<class T, std::size_t N, std::size_t M = N>
class CrabCups {
	using Vect = typename std::vector<T>;
	using Iter = typename Vect::iterator;

	template<class T_, std::size_t N_, std::size_t M_>
	friend std::ostream& operator<<(std::ostream& os, const CrabCups<T_, N_, M_>& cc);

private:
	unsigned int _moves = 0;
	const std::size_t _swapped = 3;
	Vect _data;
	Iter _it;

private:
	static T char2uint(const char c) { return c - '0'; }

public:
	CrabCups(const char(&data)[N + 1])
	{
		_data.reserve(M);
		for (std::size_t i = 0; i < N; i++)
			_data.push_back(char2uint(data[i]));
		for (std::size_t j = N; j < M; j++)
			_data.push_back(j + 1);
		_it = _data.begin();
	}

	constexpr std::size_t size() const {
		return M;
	}

	inline unsigned int get_moves() const {
		return _moves;
	}

private:
	inline Iter advance(Iter it, typename Iter::difference_type diff) {
		auto rem = diff % size();
		auto until = std::distance(it, _data.end());
		auto dist = rem < until ? std::distance(_data.begin(), it + rem) : rem - until;
		return _data.begin() + dist;
	}

	inline Iter advance(typename Iter::difference_type diff) {
		return advance(_it, diff);
	}

public:
	inline T get_current() const { return *_it; }

	inline Iter get_destination() {
		T target = get_current();
		bool end = false;
		while (!end)
		{
			target = subtract(target);
			end = true;
			for (typename Iter::difference_type i = 1; i <= _swapped; i++)
			{
				if (target == *advance(i))
				{
					end = false;
					break;
				}
			}
		}
		return std::find(_data.begin(), _data.end(), target);
	}

private:
	inline T subtract(T value) const 
	{
		auto v = value - 1;
		return v == 0 ? size() : v;
	}

	inline typename Iter::difference_type distance(Iter first, Iter last) const
	{
		auto dist = std::distance(first, last);
		if (dist > 0)
			return dist;
		else
			return M + dist;
	}

	inline Iter swap_cups() {
		Iter dest = get_destination();
		auto dist = distance(_it, dest) - _swapped;
		for (unsigned i = _swapped; i > 0; i--)
		{
			auto left = advance(_it, i);
			for (unsigned j = dist; j > 0; j--)
			{
				auto right = advance(_it, i + j);
				std::swap(*left, *right);
			}
		}
		_it = advance(_it, 1);
		return _it;
	}

public:
	inline void move() {
		_moves++;
		// spdlog::debug("-- move {}--", _moves);
		// spdlog::debug("cups: {}", *this);
		// spdlog::debug("pick up: {}, {}, {}", *advance(1), *advance(2), *advance(3));
		// spdlog::debug("destination: {}", *get_destination());
		swap_cups();
	}

	inline T find(T value, typename Iter::difference_type offset)
	{
		Iter it = std::find(_data.begin(), _data.end(), value);
		auto loc = advance(it, offset);
		return *loc;
	}

};

template<class T, std::size_t N, std::size_t M>
inline std::ostream& operator<<(std::ostream& os, const CrabCups<T, N, M>& cc)
{
	for (auto const& i : cc._data)
		if (i == cc.get_current())
			os << "(" << i << ")";
		else
			os << " " << i << " ";
	return os;
}

template<std::size_t N>
CrabCups(const char(&data)[N])->CrabCups<unsigned int, N - 1>;
