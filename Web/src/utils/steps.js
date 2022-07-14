// 定义介绍的步骤
const steps = [
    {
      target: '.mode-bar',
      header:{
        title: '欢迎来到薛定谔的猫！',
      },
      content: `选择处理模式`,
      params: {
        placement: 'bottom', // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
    }
    },
    {
        target: '#upload-btn',
        header:{
          title: '选择模式后 才可以上传文件哦',
        },
        content: `点击上传文件，支持jpg，png格式`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      // {
      //   target: '#draw-tools',
      //   header:{
      //     title: '如何裁取我想处理的区域？',
      //   },
      //   content: `您可以点击绘制工具进行绘制`,
      //   params: {
      //     placement: 'bottom' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
      //   }
      // },
      {
        target: '#process-btn',
        header:{
          title: '如何处理我的图像？',
        },
        content: `在上传文件后，点击开始处理您的图像`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      {
        target: '#analyse-btn',
        header:{
          title: '想查看处理结果初步的数据分析？',
        },
        content: `点击按钮以查看`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      {
        target: '#download-btn',
        header:{
          title: '保存至本地',
        },
        content: `点击以保存所有处理结果`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      {
        target: '#query-btn',
        header:{
          title: '下一步',
        },
        content: `点击以查看处理历史`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      {
        target: '#refresh-btn',
        header:{
          title: '刷新页面',
        },
        content: `点击以清除当前页面数据`,
        params: {
          placement: 'left' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
      {
        target: '.tip',
        header:{
          title: '再次召唤我！',
        },
        content: `如果有任何步骤遗忘，请点这里!`,
        params: {
          placement: 'bottom' // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
        }
      },
]

export default steps