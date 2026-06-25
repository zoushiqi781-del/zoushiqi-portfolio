"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useCallback, useEffect } from "react";
import Image from "next/image";

/* ─── Felt palette ─── */
const C = {
  yellow: "#F0C523",
  pink: "#E06289",
  red: "#DF4331",
  blue: "#3C8CCA",
  brown: "#5A3223",
};

/* ─── Work items ─── */
type Work = {
  id: string;
  title: string;
  sub: string;
  hint: string;
  color: string;
  className: string;
  images: string[];
  video?: string;
};

const WORKS: Work[] = [
  {
    id: "huanjiang",
    title: "秘境环江",
    sub: "毛南狂欢季",
    hint: "全国一等奖",
    color: C.red,
    className: "absolute top-[10%] left-[3%] rotate-[-5deg]",
    images: Array.from({ length: 20 }, (_, i) => `/works/huanjiang/${String(i + 1).padStart(2, "0")}.jpg`),
  },
  {
    id: "sanfu",
    title: "三福帮你搭",
    sub: "品牌策划案",
    hint: "大广赛·组长",
    color: C.blue,
    className: "absolute top-[8%] left-[27%] rotate-[3deg]",
    images: Array.from({ length: 27 }, (_, i) => `/works/sanfu/${String(i + 1).padStart(2, "0")}.jpg`),
  },
  {
    id: "unionpay",
    title: "UGO·银联",
    sub: "品牌营销策划",
    hint: "大广节",
    color: C.yellow,
    className: "absolute top-[12%] left-[51%] rotate-[-3deg]",
    images: Array.from({ length: 11 }, (_, i) => `/works/unionpay/${String(i + 1).padStart(2, "0")}.jpg`),
  },
  {
    id: "pets",
    title: "运营实践",
    sub: "小红书萌宠内容账号运营",
    hint: "爆款分析",
    color: C.pink,
    className: "absolute top-[10%] left-[72%] rotate-[4deg]",
    images: Array.from({ length: 4 }, (_, i) => `/works/pets/p${i + 1}.jpg`),
  },
  {
    id: "datamining",
    title: "蜜雪冰城",
    sub: "3·15舆情分析",
    hint: "Python数据挖掘",
    color: C.red,
    className: "absolute top-[52%] left-[5%] rotate-[4deg]",
    images: Array.from({ length: 5 }, (_, i) => `/works/datamining/d${i + 1}.jpg`),
  },
  {
    id: "rio",
    title: "Rio微醺",
    sub: "TVC 视频广告",
    hint: "学院奖",
    color: C.pink,
    className: "absolute top-[54%] left-[28%] rotate-[-4deg]",
    images: ["/works/rio/cover.png"],
    video: "/works/rio/rio.mp4",
  },
  {
    id: "kirasworld",
    title: "Kirasworld",
    sub: "个人全栈 Web 项目",
    hint: "Vibe Coding · 全栈独立开发",
    color: C.blue,
    className: "absolute top-[50%] left-[50%] rotate-[3deg]",
    images: Array.from({ length: 5 }, (_, i) => `/works/kirasworld/k${i + 1}.jpg`),
  },
];

/* ─── Work Gallery ─── */
function WorkGallery({
  work,
  onBack,
}: {
  work: Work;
  onBack: () => void;
}) {
  const [current, setCurrent] = useState(0);
  const images = work.images;
  const total = images.length;
  const goPrev = useCallback(() => setCurrent((p) => (p - 1 + total) % total), [total]);
  const goNext = useCallback(() => setCurrent((p) => (p + 1) % total), [total]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onBack();
      if (e.key === "ArrowLeft") goPrev();
      if (e.key === "ArrowRight") goNext();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onBack, goPrev, goNext]);

  /* ── Video work: play the real video instead of an image carousel ── */
  if (work.video) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] flex flex-col"
        style={{ background: "rgba(26,26,26,0.96)" }}
      >
        <div className="flex items-center justify-between px-6 py-4 shrink-0">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-white/70 hover:text-white transition-colors text-sm font-body"
          >
            <span className="text-lg">←</span> 回到房间
          </button>
          <h3 className="font-cute text-lg" style={{ color: work.color }}>{work.title}</h3>
          <span className="text-white/40 text-sm font-body">{work.hint}</span>
        </div>

        <div className="flex-1 flex items-center justify-center min-h-0 px-4 pb-6">
          <video
            src={work.video}
            poster={work.images[0]}
            controls
            autoPlay
            playsInline
            className="max-h-full max-w-5xl w-auto rounded-2xl shadow-2xl bg-black"
          />
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex flex-col"
      style={{ background: "rgba(26,26,26,0.95)" }}
    >
      <div className="flex items-center justify-between px-6 py-4 shrink-0">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-white/70 hover:text-white transition-colors text-sm font-body"
        >
          <span className="text-lg">←</span> 回到房间
        </button>
        <h3 className="font-cute text-lg" style={{ color: work.color }}>{work.title}</h3>
        <span className="text-white/40 text-sm font-body tabular-nums">
          {current + 1} / {total}
        </span>
      </div>

      <div className="flex-1 relative flex items-center justify-center min-h-0 px-4 pb-4">
        <button
          onClick={goPrev}
          className="absolute left-4 md:left-8 z-10 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 transition-all flex items-center justify-center text-white text-xl hover:scale-110"
        >
          ‹
        </button>

        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -60 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="relative w-full h-full max-w-5xl mx-auto"
          >
            <Image
              src={images[current]}
              alt={`${work.title} - ${current + 1}`}
              fill
              className="object-contain"
              sizes="(max-width: 768px) 100vw, 80vw"
            />
          </motion.div>
        </AnimatePresence>

        <button
          onClick={goNext}
          className="absolute right-4 md:right-8 z-10 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 transition-all flex items-center justify-center text-white text-xl hover:scale-110"
        >
          ›
        </button>
      </div>

      <div className="shrink-0 px-6 pb-4">
        <div className="flex gap-2 overflow-x-auto py-2 justify-center">
          {images.map((img, i) => (
            <button
              key={i}
              onClick={() => setCurrent(i)}
              className={`shrink-0 w-16 h-10 md:w-20 md:h-12 rounded-lg overflow-hidden border-2 transition-all ${
                i === current ? "border-white scale-110" : "border-transparent opacity-50 hover:opacity-80"
              }`}
            >
              <Image src={img} alt="" width={80} height={48} className="w-full h-full object-cover" />
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

/* ─── Ability Map (我的能力地图) ─── */
const COMPETENCIES = [
  { name: "品牌策划", color: C.red, desc: "能够完成品牌定位分析、传播主题提炼与营销策略构思，参与多项品牌策划与广告竞赛项目。擅长从用户洞察出发寻找传播切入点，将品牌诉求转化为具有传播性的创意概念，并形成完整策划方案。" },
  { name: "内容运营", color: C.pink, desc: "具备小红书内容运营实践经验，能够独立完成账号定位、选题策划、内容生产与数据复盘。运营萌宠内容账号期间创作多篇高互动内容，最高单篇笔记获得 3.6 万点赞，积累了对平台推荐机制与用户偏好的实际理解。" },
  { name: "文案写作", color: C.blue, desc: "擅长品牌文案、活动文案、主题 slogan、社交媒体内容与传播话题创作。能够根据不同平台与受众调整表达方式，通过标题设计、情绪表达与叙事结构提升内容传播效果与用户互动意愿。" },
  { name: "活动策划", color: C.yellow, desc: "参与节事活动、校园活动及品牌营销活动策划，具备活动主题设计、流程规划与传播方案撰写能力。能够围绕目标受众需求设计活动体验，并结合线上传播形成完整活动闭环。" },
  { name: "短视频制作", color: C.brown, desc: "具备短视频脚本创作、拍摄与剪辑能力，参与直播赛道引流短视频制作实践。能够结合平台内容特点设计传播素材，熟悉从创意构思到成片输出的完整制作流程。" },
  { name: "社媒运营", color: C.red, desc: "熟悉小红书、抖音等内容平台运营逻辑，关注用户行为与内容传播规律。能够结合热点趋势、平台活动与用户兴趣进行内容优化，并通过数据反馈持续调整运营策略。" },
  { name: "数据分析", color: C.blue, desc: "能够利用 Python 进行数据清洗、探索性分析与舆情研究，熟悉 Pandas、NumPy、Matplotlib、jieba 等工具库，掌握 LDA 主题模型、词频统计、关键词提取等文本挖掘方法。能够结合 SPSS 进行问卷数据分析，并将数据结果转化为用户洞察与传播策略建议。" },
  { name: "AI 实践", color: C.pink, desc: "熟练运用 ChatGPT、Claude、Claude Code、Codex、Gemini、Grok、Cursor 等主流工具辅助创意生产与项目开发。能够利用 AI 完成文案创作、方案优化、视觉设计辅助及网站搭建，并持续探索 AI 在营销传播领域的应用场景。" },
  { name: "视觉表达", color: C.yellow, desc: "掌握 Photoshop、Illustrator、Canva 等设计工具，能够完成海报设计、活动视觉延展与方案视觉呈现。具备基础审美与版式设计能力，能够将创意内容以更直观的形式进行表达。" },
];

const SOFTWARE_TOOLS = ["Photoshop", "Illustrator", "Premiere Pro", "Canva", "Python", "SPSS", "Office", "Figma"];
const AI_TOOLS = ["ChatGPT", "Claude", "Claude Code", "Codex", "Gemini", "Grok", "Deepseek", "Cursor", "Midjourney", "即梦"];

const EXPERIENCES: {
  period: string;
  role: string;
  desc: string;
  color: string;
  involved?: string[];
  gains: string[];
}[] = [
  {
    period: "2024.09 – 2025.06",
    role: "上海大学教务处 · 学生助理",
    desc: "协助教务处开展教学管理与学生服务工作，参与学籍事务处理、信息整理与师生沟通协调。",
    gains: ["跨部门沟通协调", "事务处理与执行", "信息整理与规范管理"],
    color: C.blue,
  },
  {
    period: "2024 – 2025",
    role: "短视频内容拍摄（兼职）",
    desc: "参与抖音直播赛道账号引流短视频拍摄与制作，多次协助主播完成内容输出，了解直播内容传播逻辑与短视频引流机制。",
    involved: ["短视频拍摄", "内容策划协助", "直播引流素材制作"],
    gains: ["短视频内容生产", "流量逻辑认知", "平台运营观察"],
    color: C.pink,
  },
  {
    period: "2025.07 – 2025.08",
    role: "作业帮 · 英语助教",
    desc: "负责小升初英语课程课后辅导与学习跟踪，开展一对一知识巩固训练，协助学生完成学习目标。",
    gains: ["内容表达与讲解", "用户沟通与反馈", "复杂信息简化能力"],
    color: C.yellow,
  },
];

function AboutPanel({ onBack }: { onBack: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-6"
      style={{ background: "rgba(26,26,26,0.92)" }}
      onClick={onBack}
    >
      <motion.div
        initial={{ scale: 0.9, y: 30 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 30 }}
        transition={{ type: "spring", damping: 25 }}
        className="bg-cream rounded-3xl p-6 md:p-10 max-w-3xl w-full max-h-[90vh] overflow-y-auto relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onBack}
          className="absolute top-4 right-4 w-10 h-10 rounded-full bg-felt-brown/10 hover:bg-felt-brown/20 flex items-center justify-center text-felt-brown transition-colors text-lg z-10"
        >
          ×
        </button>

        <h2 className="font-cute text-3xl md:text-4xl text-felt-brown mb-1">我的能力地图</h2>
        <p className="text-sm text-felt-brown/50 font-body mb-7">从创意构思到内容落地</p>

        {/* Competencies */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-5 mb-9">
          {COMPETENCIES.map((c) => (
            <div key={c.name} className="flex gap-3">
              <div className="w-1.5 rounded-full shrink-0" style={{ background: c.color }} />
              <div>
                <p className="font-cute text-lg mb-1" style={{ color: c.color }}>{c.name}</p>
                <p className="text-[13px] text-charcoal/65 font-body leading-relaxed">{c.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Education & certificates */}
        <div className="border-t border-felt-brown/10 pt-6">
          <p className="text-xs text-charcoal/30 font-body uppercase tracking-widest mb-4">教育背景与证书</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="font-body font-bold text-charcoal text-sm mb-1">教育背景</p>
              <p className="text-sm text-charcoal/65 font-body">上海大学 · 新闻传播学院 · 广告学专业</p>
              <p className="text-xs text-charcoal/40 font-body mt-0.5">2024—2028 · 本科在读</p>

              <p className="font-body font-bold text-charcoal text-sm mt-4 mb-1">语言能力</p>
              <p className="text-sm text-charcoal/65 font-body">大学英语四级（CET-4） · 六级（CET-6） · 普通话标准</p>
            </div>

            <div>
              <p className="font-body font-bold text-charcoal text-sm mb-2">软件工具</p>
              <div className="flex flex-wrap gap-1.5 mb-4">
                {SOFTWARE_TOOLS.map((s) => (
                  <span key={s} className="px-2.5 py-1 rounded-full text-[11px] font-body bg-felt-brown/8 text-felt-brown">{s}</span>
                ))}
              </div>
              <p className="font-body font-bold text-charcoal text-sm mb-2">AI 工具</p>
              <div className="flex flex-wrap gap-1.5">
                {AI_TOOLS.map((s, i) => (
                  <span key={s} className="px-2.5 py-1 rounded-full text-[11px] font-bold text-white font-body" style={{ background: [C.pink, C.blue, C.brown, C.red, C.yellow][i % 5] }}>{s}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ─── Experience Panel (经历 · 履历) ─── */
function ExperiencePanel({ onBack }: { onBack: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-6"
      style={{ background: "rgba(26,26,26,0.92)" }}
      onClick={onBack}
    >
      <motion.div
        initial={{ scale: 0.9, y: 30 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 30 }}
        transition={{ type: "spring", damping: 25 }}
        className="bg-cream rounded-3xl p-6 md:p-10 max-w-2xl w-full max-h-[90vh] overflow-y-auto relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onBack}
          className="absolute top-4 right-4 w-10 h-10 rounded-full bg-felt-brown/10 hover:bg-felt-brown/20 flex items-center justify-center text-felt-brown transition-colors text-lg z-10"
        >
          ×
        </button>

        <div className="flex items-start justify-between gap-4 mb-7 flex-wrap">
          <div>
            <h2 className="font-cute text-3xl md:text-4xl text-felt-brown mb-1">Experience</h2>
            <p className="text-sm text-felt-brown/50 font-body">在不同场景中积累内容、沟通与执行能力</p>
          </div>
          <a
            href="/resume.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 px-4 py-2 rounded-full text-sm font-bold text-white font-body transition-transform hover:scale-105"
            style={{ background: C.brown }}
          >
            ↓ 下载简历
          </a>
        </div>

        <div className="space-y-7">
          {EXPERIENCES.map((exp) => (
            <div key={exp.role} className="flex gap-4 items-start">
              <div className="w-1.5 rounded-full shrink-0 mt-1.5" style={{ background: exp.color, alignSelf: "stretch" }} />
              <div className="flex-1">
                <div className="flex items-baseline gap-2 flex-wrap">
                  <p className="font-body font-bold text-charcoal text-base">{exp.role}</p>
                  <p className="text-xs text-charcoal/35 font-body">{exp.period}</p>
                </div>
                <p className="text-sm text-charcoal/65 font-body leading-relaxed mt-1.5">{exp.desc}</p>

                {exp.involved && (
                  <div className="mt-2.5">
                    <span className="text-[11px] text-charcoal/35 font-body mr-1.5">参与内容</span>
                    {exp.involved.map((t) => (
                      <span key={t} className="inline-block mb-1 mr-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-body bg-felt-brown/8 text-felt-brown/80">{t}</span>
                    ))}
                  </div>
                )}

                <div className="mt-2">
                  <span className="text-[11px] text-charcoal/35 font-body mr-1.5">收获能力</span>
                  {exp.gains.map((t) => (
                    <span key={t} className="inline-block mb-1 mr-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold text-white font-body" style={{ background: exp.color }}>{t}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ─── Category Panel (a single object that holds several works) ─── */
function CategoryPanel({
  categoryKey,
  onOpenWork,
  onBack,
}: {
  categoryKey: CategoryKey;
  onOpenWork: (work: Work) => void;
  onBack: () => void;
}) {
  const cat = CATEGORIES[categoryKey];
  const works = cat.ids.map((id) => WORKS.find((w) => w.id === id)).filter(Boolean) as Work[];
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-6"
      style={{ background: "rgba(26,26,26,0.92)" }}
      onClick={onBack}
    >
      <motion.div
        initial={{ scale: 0.92, y: 30 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.92, y: 30 }}
        transition={{ type: "spring", damping: 25 }}
        className="bg-cream rounded-3xl p-6 md:p-10 max-w-4xl w-full max-h-[90vh] overflow-y-auto relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onBack}
          className="absolute top-4 right-4 w-10 h-10 rounded-full bg-felt-brown/10 hover:bg-felt-brown/20 flex items-center justify-center text-felt-brown transition-colors text-lg z-10"
        >
          ×
        </button>

        <h2 className="font-cute text-3xl md:text-4xl text-felt-brown mb-1">{cat.title}</h2>
        <p className="text-sm text-felt-brown/50 font-body mb-8">{cat.sub}</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {works.map((work) => (
            <WorkGridCard key={work.id} work={work} onOpen={() => onOpenWork(work)} />
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ─── Contact Panel ─── */
function ContactPanel({ onBack }: { onBack: () => void }) {
  const [showQR, setShowQR] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-6"
      style={{ background: "rgba(26,26,26,0.9)" }}
      onClick={onBack}
    >
      <motion.div
        initial={{ scale: 0.9, y: 30 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 30 }}
        transition={{ type: "spring", damping: 25 }}
        className="bg-cream rounded-3xl p-8 md:p-12 max-w-md w-full relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onBack}
          className="absolute top-4 right-4 w-10 h-10 rounded-full bg-felt-brown/10 hover:bg-felt-brown/20 flex items-center justify-center text-felt-brown transition-colors text-lg"
        >
          ×
        </button>

        <h2 className="font-cute text-4xl text-felt-brown mb-8">来找我聊聊</h2>

        <div className="space-y-4">
          <a href="mailto:zoushiqi781@gmail.com" className="block p-4 rounded-2xl bg-white/60 hover:bg-white/80 transition-colors group">
            <p className="text-xs uppercase tracking-widest mb-1 font-body" style={{ color: C.pink }}>Email</p>
            <p className="font-cute text-lg text-felt-brown">zoushiqi781@gmail.com</p>
          </a>

          <a href="tel:15270025359" className="block p-4 rounded-2xl bg-white/60 hover:bg-white/80 transition-colors group">
            <p className="text-xs uppercase tracking-widest mb-1 font-body" style={{ color: C.blue }}>Phone</p>
            <p className="font-cute text-lg text-felt-brown">152 7002 5359</p>
          </a>

          <button
            onClick={() => setShowQR(true)}
            className="w-full text-left p-4 rounded-2xl bg-white/60 hover:bg-white/80 transition-colors"
          >
            <p className="text-xs uppercase tracking-widest mb-1 font-body" style={{ color: C.yellow }}>WeChat</p>
            <p className="font-cute text-lg text-felt-brown">pigger</p>
            <p className="text-xs text-charcoal/40 font-body mt-1">点击查看二维码</p>
          </button>
        </div>

        <AnimatePresence>
          {showQR && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-[200] flex items-center justify-center bg-black/60 backdrop-blur-sm"
              onClick={() => setShowQR(false)}
            >
              <motion.div
                initial={{ scale: 0.5 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.5 }}
                transition={{ type: "spring", damping: 20 }}
                className="bg-white rounded-3xl p-6 shadow-2xl"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="relative w-64 h-64 mx-auto mb-4">
                  <Image src="/wechat-qr.jpg" alt="微信二维码" fill className="object-contain rounded-xl" />
                </div>
                <p className="text-center font-cute text-felt-brown">扫码加我微信</p>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}

/* ─── Work Grid Card (default recruiter-friendly view) ─── */
function WorkGridCard({
  work,
  onOpen,
}: {
  work: Work;
  onOpen: () => void;
}) {
  const hasContent = work.images.length > 0;

  return (
    <motion.button
      type="button"
      onClick={hasContent ? onOpen : undefined}
      disabled={!hasContent}
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={`group relative text-left rounded-3xl overflow-hidden bg-white shadow-[0_4px_24px_rgba(90,50,35,0.08)] transition-all duration-300 ${
        hasContent
          ? "cursor-pointer hover:-translate-y-1.5 hover:shadow-[0_18px_44px_rgba(90,50,35,0.18)]"
          : "cursor-default"
      }`}
    >
      {/* cover */}
      <div className="relative aspect-[4/3] overflow-hidden" style={{ background: `${work.color}12` }}>
        {hasContent ? (
          <Image
            src={work.images[0]}
            alt={work.title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-105"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3">
            <span className="font-cute text-2xl md:text-3xl" style={{ color: work.color }}>
              {work.title}
            </span>
            <span
              className="text-[11px] font-body font-bold px-3 py-1 rounded-full text-white"
              style={{ background: work.color }}
            >
              敬请期待
            </span>
          </div>
        )}

        {/* play overlay for video works */}
        {work.video && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="w-14 h-14 rounded-full bg-white/85 flex items-center justify-center shadow-lg transition-transform duration-300 group-hover:scale-110">
              <div
                className="w-0 h-0 ml-1"
                style={{ borderTop: "11px solid transparent", borderBottom: "11px solid transparent", borderLeft: `18px solid ${work.color}` }}
              />
            </div>
          </div>
        )}

        {hasContent && (
          <div
            className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-[11px] font-bold text-white shadow-sm"
            style={{ background: work.color }}
          >
            {work.video ? "▶ 视频" : `${work.images.length} 页`}
          </div>
        )}
      </div>

      {/* info */}
      <div className="p-5">
        <div className="flex items-baseline gap-2 flex-wrap mb-2">
          <h3 className="font-cute text-xl md:text-2xl leading-tight" style={{ color: work.color }}>
            {work.title}
          </h3>
          <span className="text-xs text-charcoal/40 font-body">{work.sub}</span>
        </div>
        <span
          className="inline-block px-3 py-1 rounded-full text-[11px] font-bold text-white font-body"
          style={{ background: work.color }}
        >
          {work.hint}
        </span>
      </div>
    </motion.button>
  );
}

/* ─── Grid View ─── */
/* ─── Interactive felt room ─── */
/* Dedicated empty-room background (3:2). */
const ROOM_BG = "/room-bg.jpg";

type CategoryKey = "planning" | "tech";

/* multi-work categories opened from a single object */
const CATEGORIES: Record<CategoryKey, { title: string; sub: string; ids: string[] }> = {
  planning: { title: "营销策划案", sub: "品牌策划 · 整合营销 · 创意提案", ids: ["huanjiang", "sanfu", "unionpay"] },
  tech: { title: "技术 · 数据", sub: "数据挖掘 · Vibe Coding", ids: ["datamining", "kirasworld"] },
};

type RoomAction =
  | { kind: "category"; key: CategoryKey }
  | { kind: "work"; id: string }
  | { kind: "about" }
  | { kind: "experience" }
  | { kind: "contact" };

type RoomObject = {
  id: string;
  label: string;
  idle: string;
  hover: string;
  /* position + size as % of the room, so it scales with the viewport */
  left: number;
  top: number;
  width: number;
  action: RoomAction;
};

/* positions are % of the room stage, matched to the reference room layout.
   each object opens its OWN content. */
const ROOM_OBJECTS: RoomObject[] = [
  { id: "box", label: "营销策划案", idle: "/objects/obj4_idle.png", hover: "/objects/obj4_hover.png", left: 30, top: 37, width: 20, action: { kind: "category", key: "planning" } },
  { id: "envelope", label: "联系我", idle: "/objects/obj3_idle.png", hover: "/objects/obj3_hover.png", left: 50, top: 25, width: 14, action: { kind: "contact" } },
  { id: "scratch", label: "小红书运营", idle: "/objects/obj7_idle.png", hover: "/objects/obj7_hover.png", left: 72, top: 27, width: 12, action: { kind: "work", id: "pets" } },
  { id: "yarn", label: "Experience", idle: "/objects/obj6_idle.png", hover: "/objects/obj6_hover.png", left: 15, top: 55, width: 19, action: { kind: "experience" } },
  { id: "jar", label: "能力地图", idle: "/objects/obj5_idle.png", hover: "/objects/obj5_hover.png", left: 16, top: 79, width: 16, action: { kind: "about" } },
  { id: "wand", label: "视频广告", idle: "/objects/obj2_idle.png", hover: "/objects/obj2_hover.png", left: 57, top: 80, width: 17, action: { kind: "work", id: "rio" } },
  { id: "orb", label: "技术 · 数据", idle: "/objects/obj1_idle.png", hover: "/objects/obj1_hover.png", left: 80, top: 76, width: 17, action: { kind: "category", key: "tech" } },
];

function RoomItem({ obj, onActivate }: { obj: RoomObject; onActivate: (a: RoomAction) => void }) {
  const labelAbove = obj.top > 65; // bottom-row objects show the label above so it isn't clipped
  return (
    <motion.button
      type="button"
      onClick={() => onActivate(obj.action)}
      className="group absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer outline-none"
      style={{ left: `${obj.left}%`, top: `${obj.top}%`, width: `${obj.width}%` }}
      animate={{ y: [0, -8, 0] }}
      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.97 }}
      aria-label={obj.label}
    >
      <div className="relative w-full transition-transform duration-300">
        {/* idle / hover cross-fade via CSS :hover */}
        <img src={obj.idle} alt="" className="w-full h-auto select-none pointer-events-none drop-shadow-[0_8px_16px_rgba(0,0,0,0.35)] transition-opacity duration-300 group-hover:opacity-0" draggable={false} />
        <img
          src={obj.hover}
          alt=""
          className="absolute inset-0 w-full h-auto select-none pointer-events-none opacity-0 transition-opacity duration-300 group-hover:opacity-100 drop-shadow-[0_12px_26px_rgba(0,0,0,0.45)]"
          draggable={false}
        />
      </div>
      {/* label tooltip — above for bottom-row objects so it isn't clipped */}
      <span
        className={`absolute left-1/2 -translate-x-1/2 whitespace-nowrap px-3 py-1 rounded-full text-xs font-bold font-body text-felt-brown bg-cream/95 shadow-md opacity-0 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0 ${
          labelAbove ? "bottom-full mb-2 translate-y-1.5" : "top-full mt-2 -translate-y-1.5"
        }`}
      >
        {obj.label}
      </span>
    </motion.button>
  );
}

function ObjectsRoom({
  onActivate,
}: {
  onActivate: (a: RoomAction) => void;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 overflow-hidden bg-[#17110d]"
    >
      {/* 3:2 stage sized to COVER the viewport (no letterbox bars); objects align to the bg */}
      <div
        className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
        style={{ width: "max(100vw, 150vh)", height: "max(66.67vw, 100vh)" }}
      >
        <img src={ROOM_BG} alt="" className="absolute inset-0 w-full h-full object-cover select-none" draggable={false} />

        {/* hint */}
        <p className="absolute top-[6%] left-1/2 -translate-x-1/2 text-center font-cute text-lg md:text-2xl text-white/45 pointer-events-none select-none">
          把光标移到小物件上看看 · 点击进入
        </p>

        {ROOM_OBJECTS.map((obj) => (
          <RoomItem key={obj.id} obj={obj} onActivate={onActivate} />
        ))}
      </div>
    </motion.div>
  );
}

/* ─── Main Page ─── */
type Overlay =
  | { type: "none" }
  | { type: "gallery"; work: Work }
  | { type: "category"; key: CategoryKey }
  | { type: "about" }
  | { type: "experience" }
  | { type: "contact" }
  | { type: "back-cover" };

export default function Home() {
  const [showCover, setShowCover] = useState(true);
  const [overlay, setOverlay] = useState<Overlay>({ type: "none" });
  const closeOverlay = useCallback(() => setOverlay({ type: "none" }), []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape" && overlay.type !== "none") closeOverlay();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [overlay, closeOverlay]);

  return (
    <main className="relative min-h-screen bg-cream">
      {/* ── The felt room IS the home (right after the cover) ── */}
      <ObjectsRoom
        onActivate={(a) => {
          if (a.kind === "category") setOverlay({ type: "category", key: a.key });
          else if (a.kind === "about") setOverlay({ type: "about" });
          else if (a.kind === "experience") setOverlay({ type: "experience" });
          else if (a.kind === "contact") setOverlay({ type: "contact" });
          else if (a.kind === "work") {
            const w = WORKS.find((x) => x.id === a.id);
            if (w) setOverlay({ type: "gallery", work: w });
          }
        }}
      />

      {/* ── Bottom bar (over the dark room) ── */}
      <div className="fixed bottom-0 left-0 right-0 z-30 flex items-center justify-center py-3 gap-4">
        <p className="text-[10px] text-white/35 font-body pointer-events-none">
          © 2026 邹诗琪 · 一只猫 · ∞个想法
        </p>
        <button
          onClick={() => setOverlay({ type: "back-cover" })}
          className="text-[10px] text-white/45 hover:text-white/80 font-body transition-colors underline underline-offset-2"
        >
          封底
        </button>
      </div>

      {/* ── Cover (initial splash) ── */}
      <AnimatePresence>
        {showCover && (
          <motion.div
            key="cover"
            className="fixed inset-0 z-[120] cursor-pointer"
            onClick={() => setShowCover(false)}
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Image src="/fufu-hero.png" alt="封面" fill className="object-cover" priority />
            {/* scrim for legibility over the colourful felt */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/45 to-black/10" />

            <motion.div
              className="absolute inset-x-0 bottom-8 md:bottom-12 px-6 flex flex-col items-center text-center"
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.35, duration: 0.7 }}
            >
              <h1 className="font-cute text-5xl md:text-7xl text-white drop-shadow-[0_2px_12px_rgba(0,0,0,0.6)] leading-none">
                邹诗琪
              </h1>

              <p className="mt-3 font-body text-[11px] md:text-sm text-white/85 tracking-[0.18em]">
                上海大学 · 新闻传播学院 · 广告学专业 · 2028届
              </p>

              <p className="mt-3 font-cute text-xl md:text-3xl drop-shadow-[0_2px_8px_rgba(0,0,0,0.5)]">
                <span style={{ color: C.yellow }}>品牌策划</span>
                <span className="text-white/40 mx-1.5">｜</span>
                <span style={{ color: C.pink }}>内容运营</span>
                <span className="text-white/40 mx-1.5">｜</span>
                <span style={{ color: C.blue }}>AI实践</span>
              </p>

              {/* achievements with simple line icons (no emoji) */}
              <div className="mt-5 flex flex-wrap justify-center items-center gap-x-5 gap-y-2.5 font-body text-xs md:text-sm">
                <span className="flex items-center gap-1.5 text-white/95" style={{ textShadow: "0 1px 6px rgba(0,0,0,0.6)" }}>
                  <svg viewBox="0 0 24 24" fill="none" stroke={C.yellow} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
                    <path d="M7 4h10v4a5 5 0 0 1-10 0V4Z" /><path d="M5 6H4a2 2 0 0 0 0 4h1" /><path d="M19 6h1a2 2 0 0 1 0 4h-1" /><path d="M12 17v3" /><path d="M8 21h8" />
                  </svg>
                  策划案全国一等奖
                </span>
                <span className="flex items-center gap-1.5 text-white/95" style={{ textShadow: "0 1px 6px rgba(0,0,0,0.6)" }}>
                  <svg viewBox="0 0 24 24" fill="none" stroke={C.pink} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
                    <path d="M12 3c.6 2.4 2.8 3.4 2.8 6.2a2.8 2.8 0 0 1-5.6 0c0-.9.3-1.5.8-2.1.3 1.2 1.4 1.3 1.4.2 0-1.4-.9-2.6.6-4.3Z" /><path d="M8.5 13.5a3.5 3.5 0 1 0 7 0c0-1-.4-1.8-1-2.5" />
                  </svg>
                  多条爆款内容
                </span>
                <span className="flex items-center gap-1.5 text-white/95" style={{ textShadow: "0 1px 6px rgba(0,0,0,0.6)" }}>
                  <svg viewBox="0 0 24 24" fill="none" stroke={C.blue} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
                    <path d="M3 20h18" /><path d="M6 20v-6" /><path d="M11 20V8" /><path d="M16 20v-9" /><path d="M20.5 20v-4" />
                  </svg>
                  Python数据分析
                </span>
                <span className="flex items-center gap-1.5 text-white/95" style={{ textShadow: "0 1px 6px rgba(0,0,0,0.6)" }}>
                  <svg viewBox="0 0 24 24" fill="none" stroke={C.red} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-[18px] h-[18px]">
                    <path d="M9 8l-4 4 4 4" /><path d="M15 8l4 4-4 4" />
                  </svg>
                  AI网站开发
                </span>
              </div>

              <p className="mt-5 font-body text-xs md:text-sm text-white/80 leading-relaxed max-w-md" style={{ textShadow: "0 1px 6px rgba(0,0,0,0.55)" }}>
                从品牌策划到内容运营，从数据分析到AI开发，<br className="hidden md:block" />我喜欢把想法变成真实可见的作品。
              </p>

              <motion.p
                className="mt-7 text-white/75 text-xs font-body tracking-widest"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                点击任意处进入
              </motion.p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Overlay Views ── */}
      <AnimatePresence>
        {overlay.type === "gallery" && <WorkGallery work={overlay.work} onBack={closeOverlay} />}
        {overlay.type === "category" && (
          <CategoryPanel
            categoryKey={overlay.key}
            onOpenWork={(work) => setOverlay({ type: "gallery", work })}
            onBack={closeOverlay}
          />
        )}
        {overlay.type === "about" && <AboutPanel onBack={closeOverlay} />}
        {overlay.type === "experience" && <ExperiencePanel onBack={closeOverlay} />}
        {overlay.type === "contact" && <ContactPanel onBack={closeOverlay} />}
        {overlay.type === "back-cover" && (
          <motion.div
            key="back-cover"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] cursor-pointer"
            onClick={closeOverlay}
          >
            <Image src="/fufu-footer.png" alt="封底" fill className="object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent" />
            <motion.div
              className="absolute bottom-12 left-1/2 -translate-x-1/2 text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <p className="font-cute text-white/90 text-2xl md:text-4xl mb-2">谢谢观看</p>
              <p className="text-white/50 text-sm font-body">邹诗琪 · 一只猫 · ∞个想法</p>
              <motion.p
                className="text-white/40 text-xs font-body mt-4"
                animate={{ opacity: [0.3, 0.8, 0.3] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                点击返回
              </motion.p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
