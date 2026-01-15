
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Terminal-like resolution
#define CHAR_COLS 160
#define CHAR_ROWS 44

// Font glyph size (pixels)
#define GLYPH_W 8
#define GLYPH_H 8

// Window pixel size (texture will be CHAR_COLS*GLYPH_W x CHAR_ROWS*GLYPH_H)
const int WIN_W = CHAR_COLS * GLYPH_W; // 1280
const int WIN_H = CHAR_ROWS * GLYPH_H; // 352

// ASCII buffer & z-buffer
static float zBuffer[CHAR_COLS * CHAR_ROWS];
static unsigned char charBuffer[CHAR_COLS * CHAR_ROWS]; // stores ASCII code
static const unsigned char backgroundASCIICode = '.';

// Cubes parameters (kept from original)
static float A = 0.0f, B = 0.0f, C = 0.0f;
static float cubeWidth = 20.0f;
static int width_chars = CHAR_COLS;
static int height_chars = CHAR_ROWS;
static float distanceFromCam = 100.0f;
static float horizontalOffset = 0.0f;
static float K1 = 40.0f;
static float incrementSpeed = 0.6f;

// Temp per-surface
static float x_, y_, z_;
static float ooz;
static int xp, yp;
static int idx_;

// Simple helper to sleep milliseconds (cross-platform)
static void sleep_ms(int ms) {
#ifdef _WIN32
    Sleep(ms);
#else
    struct timespec req = { ms / 1000, (ms % 1000) * 1000000 };
    nanosleep(&req, NULL);
#endif
}

// ========== Small 8x8 bitmap font for the chars we use =========
// Each glyph is 8 bytes (rows), LSB is leftmost pixel. 1 => pixel on.
typedef unsigned char GlyphRow;
typedef struct { char ch; GlyphRow rows[GLYPH_H]; } GlyphEntry;

// We only need glyphs for: '@', '$', '~', '#', ';', '+', '.' and space.
// Glyph patterns are simple approximations (not full font).
static GlyphEntry glyphs[] = {
    // '@' approximate
    {'@', {0x3C,0x42,0x9D,0x9D,0x9B,0x40,0x3C,0x00}},
    // '$' approximate
    {'$', {0x08,0x3E,0x28,0x3C,0x0A,0x3E,0x08,0x00}},
    // '~' approximate (wavy)
    {'~', {0x00,0x00,0x18,0x24,0x12,0x00,0x00,0x00}},
    // '#' hash
    {'#', {0x00,0x24,0x7E,0x24,0x7E,0x24,0x00,0x00}},
    // ';' semicolon (dot + short vertical)
    {';', {0x00,0x00,0x18,0x18,0x18,0x10,0x10,0x08}},
    // '+' plus
    {'+', {0x00,0x08,0x08,0x3E,0x08,0x08,0x00,0x00}},
    // '.' dot
    {'.', {0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00}},
    // ' ' space
    {' ', {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}},
};

// Find glyph by char (linear search small table)
static const GlyphRow* find_glyph(char c) {
    for (size_t i = 0; i < sizeof(glyphs)/sizeof(glyphs[0]); ++i) {
        if (glyphs[i].ch == c) return glyphs[i].rows;
    }
    return NULL;
}

// ========== Soft ASCII projection math (copied from original) ==========
static float calculateX(int i, int j, int k) {
    return j * sinf(A) * sinf(B) * cosf(C) - k * cosf(A) * sinf(B) * cosf(C) +
           j * cosf(A) * sinf(C) + k * sinf(A) * sinf(C) + i * cosf(B) * cosf(C);
}

static float calculateY(int i, int j, int k) {
    return j * cosf(A) * cosf(C) + k * sinf(A) * cosf(C) -
           j * sinf(A) * sinf(B) * sinf(C) + k * cosf(A) * sinf(B) * sinf(C) -
           i * cosf(B) * sinf(C);
}

static float calculateZ(int i, int j, int k) {
    return k * cosf(A) * cosf(B) - j * sinf(A) * cosf(B) + i * sinf(B);
}

static void calculateForSurface(float cubeX, float cubeY, float cubeZ, int ch) {
    x_ = calculateX((int)cubeX, (int)cubeY, (int)cubeZ);
    y_ = calculateY((int)cubeX, (int)cubeY, (int)cubeZ);
    z_ = calculateZ((int)cubeX, (int)cubeY, (int)cubeZ) + distanceFromCam;

    ooz = 1.0f / z_;

    xp = (int)(width_chars / 2 + horizontalOffset + K1 * ooz * x_ * 2.0f);
    yp = (int)(height_chars / 2 + K1 * ooz * y_);

    idx_ = xp + yp * width_chars;
    if (idx_ >= 0 && idx_ < width_chars * height_chars) {
        if (ooz > zBuffer[idx_]) {
            zBuffer[idx_] = ooz;
            charBuffer[idx_] = (unsigned char)ch;
        }
    }
}

// Fill buffers just like original example (three cubes)
static void render_ascii_cubes_to_buffer() {
    // clear
    for (int i = 0; i < width_chars * height_chars; ++i) {
        zBuffer[i] = 0.0f;
        charBuffer[i] = backgroundASCIICode;
    }

    cubeWidth = 20.0f;
    horizontalOffset = -2.0f * cubeWidth;
    for (float cubeX = -cubeWidth; cubeX < cubeWidth; cubeX += incrementSpeed) {
        for (float cubeY = -cubeWidth; cubeY < cubeWidth; cubeY += incrementSpeed) {
            calculateForSurface(cubeX, cubeY, -cubeWidth, '@');
            calculateForSurface(cubeWidth, cubeY, cubeX, '$');
            calculateForSurface(-cubeWidth, cubeY, -cubeX, '~');
            calculateForSurface(-cubeX, cubeY, cubeWidth, '#');
            calculateForSurface(cubeX, -cubeWidth, -cubeY, ';');
            calculateForSurface(cubeX, cubeWidth, cubeY, '+');
        }
    }

    cubeWidth = 10.0f;
    horizontalOffset = 1.0f * cubeWidth;
    for (float cubeX = -cubeWidth; cubeX < cubeWidth; cubeX += incrementSpeed) {
        for (float cubeY = -cubeWidth; cubeY < cubeWidth; cubeY += incrementSpeed) {
            calculateForSurface(cubeX, cubeY, -cubeWidth, '@');
            calculateForSurface(cubeWidth, cubeY, cubeX, '$');
            calculateForSurface(-cubeWidth, cubeY, -cubeX, '~');
            calculateForSurface(-cubeX, cubeY, cubeWidth, '#');
            calculateForSurface(cubeX, -cubeWidth, -cubeY, ';');
            calculateForSurface(cubeX, cubeWidth, cubeY, '+');
        }
    }

    cubeWidth = 5.0f;
    horizontalOffset = 8.0f * cubeWidth;
    for (float cubeX = -cubeWidth; cubeX < cubeWidth; cubeX += incrementSpeed) {
        for (float cubeY = -cubeWidth; cubeY < cubeWidth; cubeY += incrementSpeed) {
            calculateForSurface(cubeX, cubeY, -cubeWidth, '@');
            calculateForSurface(cubeWidth, cubeY, cubeX, '$');
            calculateForSurface(-cubeWidth, cubeY, -cubeX, '~');
            calculateForSurface(-cubeX, cubeY, cubeWidth, '#');
            calculateForSurface(cubeX, -cubeWidth, -cubeY, ';');
            calculateForSurface(cubeX, cubeWidth, cubeY, '+');
        }
    }
}

// ========== GL shader sources (simple textured quad) ==========
static const char* vs_src =
"#version 330 core\n"
"layout(location=0) in vec2 aPos;\n"
"layout(location=1) in vec2 aUV;\n"
"out vec2 vUV;\n"
"void main(){ vUV = aUV; gl_Position = vec4(aPos, 0.0, 1.0); }\n";

static const char* fs_src =
"#version 330 core\n"
"in vec2 vUV;\n"
"out vec4 FragColor;\n"
"uniform sampler2D uTex;\n" 
"void main(){ FragColor = texture(uTex, vUV); }\n";

// Helper to compile shader
static GLuint compile_shader(GLenum type, const char* src) {
    GLuint s = glCreateShader(type);
    glShaderSource(s, 1, &src, NULL);
    glCompileShader(s);
    GLint ok; glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        GLint len = 0; glGetShaderiv(s, GL_INFO_LOG_LENGTH, &len);
        if (len > 0) {
            char* buf = (char*)malloc(len);
            glGetShaderInfoLog(s, len, NULL, buf);
            fprintf(stderr, "Shader compile error: %s\n", buf);
            free(buf);
        } else fprintf(stderr, "Shader compile failed (no log)\n");
    }
    return s;
}
static GLuint link_program(GLuint vs, GLuint fs) {
    GLuint p = glCreateProgram();
    glAttachShader(p, vs);
    glAttachShader(p, fs);
    glLinkProgram(p);
    GLint ok; glGetProgramiv(p, GL_LINK_STATUS, &ok);
    if (!ok) {
        GLint len = 0; glGetProgramiv(p, GL_INFO_LOG_LENGTH, &len);
        if (len > 0) {
            char* buf = (char*)malloc(len);
            glGetProgramInfoLog(p, len, NULL, buf);
            fprintf(stderr, "Program link error: %s\n", buf);
            free(buf);
        } else fprintf(stderr, "Program link failed (no log)\n");
    }
    return p;
}

// Create an RGBA pixel buffer for the whole texture (WIN_W x WIN_H)
static unsigned char* texPixels = NULL;

// Fill texPixels using charBuffer and glyphs (white glyph on black bg)
static void build_texture_from_charbuffer() {
    int texW = CHAR_COLS * GLYPH_W;
    int texH = CHAR_ROWS * GLYPH_H;
    // fill black
    memset(texPixels, 0, texW * texH * 4);

    for (int cy = 0; cy < CHAR_ROWS; ++cy) {
        for (int cx = 0; cx < CHAR_COLS; ++cx) {
            unsigned char ch = charBuffer[cx + cy * CHAR_COLS];
            const GlyphRow* g = find_glyph((char)ch);
            if (!g) g = find_glyph(' '); // fallback
            // top-left pixel of this glyph in texture
            int px = cx * GLYPH_W;
            int py = cy * GLYPH_H;
            for (int gy = 0; gy < GLYPH_H; ++gy) {
                GlyphRow row = g[gy];
                for (int gx = 0; gx < GLYPH_W; ++gx) {
                    int bit = (row >> (7 - gx)) & 1;
                    int tx = px + gx;
                    int ty = py + gy;
                    int tidx = (ty * texW + tx) * 4;
                    if (bit) {
                        // white opaque pixel (you can change color here)
                        texPixels[tidx + 0] = 255;
                        texPixels[tidx + 1] = 255;
                        texPixels[tidx + 2] = 255;
                        texPixels[tidx + 3] = 255;
                    } else {
                        // leave transparent / black
                        texPixels[tidx + 0] = 0;
                        texPixels[tidx + 1] = 0;
                        texPixels[tidx + 2] = 0;
                        texPixels[tidx + 3] = 255; // opaque black background
                    }
                }
            }
        }
    }
}

int main(void) {
    // init glfw
    if (!glfwInit()) {
        fprintf(stderr, "GLFW init failed\n");
        return -1;
    }
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // create window sized to texture
    GLFWwindow* window = glfwCreateWindow(WIN_W, WIN_H, "ASCII Cube (in-window)", NULL, NULL);
    if (!window) {
        fprintf(stderr, "Window creation failed\n");
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // init glew
    glewExperimental = GL_TRUE;
    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "GLEW init failed\n");
        glfwTerminate();
        return -1;
    }

    // create shader program
    GLuint vs = compile_shader(GL_VERTEX_SHADER, vs_src);
    GLuint fs = compile_shader(GL_FRAGMENT_SHADER, fs_src);
    GLuint prog = link_program(vs, fs);
    glDeleteShader(vs); glDeleteShader(fs);

    // quad (two triangles) covering NDC [-1,1]
    float quadVerts[] = {
        // pos.x pos.y   u   v
        -1.0f, -1.0f,   0.0f, 0.0f,
         1.0f, -1.0f,   1.0f, 0.0f,
        -1.0f,  1.0f,   0.0f, 1.0f,
         1.0f,  1.0f,   1.0f, 1.0f,
    };
    GLuint quadVAO=0, quadVBO=0;
    glGenVertexArrays(1, &quadVAO);
    glGenBuffers(1, &quadVBO);
    glBindVertexArray(quadVAO);
    glBindBuffer(GL_ARRAY_BUFFER, quadVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(quadVerts), quadVerts, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0); glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,4*sizeof(float),(void*)0);
    glEnableVertexAttribArray(1); glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,4*sizeof(float),(void*)(2*sizeof(float)));
    glBindVertexArray(0);

    // create RGBA texture
    int texW = CHAR_COLS * GLYPH_W;
    int texH = CHAR_ROWS * GLYPH_H;
    texPixels = (unsigned char*)malloc(texW * texH * 4);
    memset(texPixels, 0, texW * texH * 4);

    GLuint tex = 0;
    glGenTextures(1, &tex);
    glBindTexture(GL_TEXTURE_2D, tex);
    // allocate once
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texW, texH, 0, GL_RGBA, GL_UNSIGNED_BYTE, texPixels);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); // keep pixel look
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glBindTexture(GL_TEXTURE_2D, 0);

    // uniform location
    glUseProgram(prog);
    glUniform1i(glGetUniformLocation(prog, "uTex"), 0);
    glUseProgram(0);

    // initial clear buffers
    for (int i=0;i<CHAR_COLS*CHAR_ROWS;i++){
        zBuffer[i] = 0.0f;
        charBuffer[i] = backgroundASCIICode;
    }

    // main loop timing
    double lastTime = glfwGetTime();
    const double target_dt = 1.0/60.0; // ~60 FPS
    while (!glfwWindowShouldClose(window)) {
        double t = glfwGetTime();
        double dt = t - lastTime;
        if (dt < target_dt) {
            // sleep a bit to be friendly
            sleep_ms((int)((target_dt - dt)*1000.0));
            t = glfwGetTime();
            dt = t - lastTime;
        }
        lastTime = t;

        // update ascii logic (same as original)
        render_ascii_cubes_to_buffer();

        // update rotations (same increments as original)
        A += 0.05f;
        B += 0.05f;
        C += 0.01f;

        // build texture from charBuffer -> texPixels
        build_texture_from_charbuffer();

        // upload to GPU (fast subimage upload)
        glBindTexture(GL_TEXTURE_2D, tex);
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, texW, texH, GL_RGBA, GL_UNSIGNED_BYTE, texPixels);
        glBindTexture(GL_TEXTURE_2D, 0);

        // draw
        int fbW, fbH;
        glfwGetFramebufferSize(window, &fbW, &fbH);
        glViewport(0,0,fbW,fbH);
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(prog);
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, tex);
        glBindVertexArray(quadVAO);
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
        glBindVertexArray(0);
        glBindTexture(GL_TEXTURE_2D, 0);
        glUseProgram(0);

        // poll events & swap
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // cleanup
    if (tex) glDeleteTextures(1, &tex);
    if (quadVBO) glDeleteBuffers(1, &quadVBO);
    if (quadVAO) glDeleteVertexArrays(1, &quadVAO);
    if (prog) glDeleteProgram(prog);

    if (texPixels) free(texPixels);

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
