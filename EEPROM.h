#ifndef EEPROM_H
#define EEPROM_H

#include <Arduino.h>
#include <stddef.h>
#include <stdint.h>

class EEPROMClass {
public:
    EEPROMClass();
    ~EEPROMClass();

    void begin(size_t size = 256);
    uint8_t read(int idx);
    void write(int idx, uint8_t val);
    bool commit();
    void end();

    template <typename T>
    T &get(int idx, T &t) {
        uint8_t *ptr = (uint8_t *)&t;
        for (size_t i = 0; i < sizeof(T); i++) {
            ptr[i] = read(idx + i);
        }
        return t;
    }

    template <typename T>
    const T &put(int idx, const T &t) {
        const uint8_t *ptr = (const uint8_t *)&t;
        for (size_t i = 0; i < sizeof(T); i++) {
            write(idx + i, ptr[i]);
        }
        return t;
    }

    uint8_t& operator[](int idx);

private:
    uint8_t *_buffer;
    size_t _size;
    bool _dirty;
};

extern EEPROMClass EEPROM;

#endif // EEPROM_H
