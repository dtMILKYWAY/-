// src/config/particles-config.ts

import type { ISourceOptions } from "tsparticles-engine";

export const options: ISourceOptions = {
  // 背景设置，这里设置为透明，以便显示我们原来的渐变色
  background: {
    color: {
      value: "transparent",
    },
  },
  // 粒子密度
  fpsLimit: 120,
  // 交互设置
  interactivity: {
    events: {
      onClick: {
        enable: true,
        mode: "push",
      },
      onHover: {
        enable: true,
        mode: "repulse",
      },
      resize: true,
    },
    modes: {
      push: {
        quantity: 4,
      },
      repulse: {
        distance: 150,
        duration: 0.4,
      },
    },
  },
  // 粒子本身设置
  particles: {
    color: {
      value: "#ffffff", // 粒子颜色
    },
    // 粒子连接线
    links: {
      color: "#ffffff",
      distance: 150,
      enable: true,
      opacity: 0.5,
      width: 1,
    },
    // 粒子碰撞
    collisions: {
        enable: true,
    },
    // 粒子移动
    move: {
      direction: "none",
      enable: true,
      outModes: {
        default: "bounce",
      },
      random: false,
      speed: 2, // 移动速度
      straight: false,
    },
    // 粒子数量
    number: {
      density: {
        enable: true,
        area: 800,
      },
      value: 80, // 粒子基础数量
    },
    // 粒子透明度
    opacity: {
      value: 0.5,
    },
    // 粒子形状
    shape: {
      type: "circle",
    },
    // 粒子大小
    size: {
      value: { min: 1, max: 5 },
    },
  },
  detectRetina: true,
};