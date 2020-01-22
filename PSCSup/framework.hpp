#pragma once

#include <cstdio>
#include <string>
#include <type_traits>
#include <memory>

#include "record/record.hpp"
#include "record/waveform_record.hpp"

#include "device.hpp"

class PrintWaveform : public WaveformRecord<double> {
public:
    PrintWaveform() = default;
    ~PrintWaveform() override = default;

    void read(double *data, size_t count) override {
        printf("count: %zd\n", count);
        printf("data: [ ");
        for (int i = 0; i < int(count); ++i) {
            printf("%lf, ", data[i]);
        }
        printf("]\n");
    }
};

template <class R>
std::unique_ptr<R> framework_init_record(const std::string &name) {
    assert(false);
}

template <>
std::unique_ptr<GenericWaveformRecord> framework_init_record(const std::string &name) {
    if (name.compare("WAVEFORM") == 0) {
        // FIXME: Call this only once
        return std::make_unique<PrintWaveform>();
    } else {
        assert(false);
    }
}

#ifdef UNITTEST
#include <catch/catch.hpp>

TEST_CASE( "Dummy test", "[dummy]" ) {
    REQUIRE(1 + 1 == 2);
}
#endif //UNITTEST
