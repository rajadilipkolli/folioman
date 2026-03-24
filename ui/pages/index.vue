<template lang="pug">
  .container
    .flex.flex-row.justify-end.items-center
      .text-base.text-secondary.mr-4 Portfolio :
      Dropdown(v-model="selectedPortfolio" :options="portfolios"
               optionLabel="name" placeholder="Select portfolio"
               @input="changePortfolio")
    .grid.grid-cols-5.gap-4.mb-4(style="min-height: 400px;")
      Card.summary.col-span-2.m-2
        template(#content)
          .summary-title-main Current Value
          .summary-value-main {{ formatCurrency(summary.totalValue) }}
          .grid.grid-cols-2.gap-8.mt-16
            .col-span-1
              .summary-title-sub Invested
              .summary-value-sub {{ formatCurrency(summary.totalInvested) }}
            .col-span-1
              .summary-title-sub No. of Funds
              .summary-value-sub {{ schemes.length }}
            .col-span-1
              .summary-title-sub Current Return
              .flex.flex-row.justify-center.items-center
                .text-white.text-xl.mr-2 {{ formatCurrency(summary.totalChange.A)  }}
                template(v-if="summary.totalChange.A >= 0")
                  .text-white.text-sm.text-green-400.font-medium +{{ formatPct(summary.totalChangePct.A) }}
                template(v-else)
                  .text-white.text-sm.text-red-400.font-medium -{{ formatPct(summary.totalChangePct.A) }}
            .col-span-1
              .summary-title-sub 1 Day Change
              .flex.flex-row.justify-center.items-center
                .text-white.text-xl.mr-2 {{ formatCurrency(summary.totalChange.D)  }}
                template(v-if="summary.totalChange.D >= 0")
                  .text-white.text-sm.text-green-400.font-medium +{{ formatPct(summary.totalChangePct.D) }}
                template(v-else)
                  .text-white.text-sm.text-red-400.font-medium {{ formatPct(summary.totalChangePct.D) }}
            .col-span-1
              .summary-title-sub Absolute XIRR
              .summary-value-sub {{ formatPct(summary.xirr.overall) }}
            .col-span-1
              .summary-title-sub Current XIRR
              .summary-value-sub {{ formatPct(summary.xirr.current) }}
        template(#footer)
          .w-full.text-right.text-gray-400.text-sm(:class="{'invisible': summary.portfolioDate === ''}") NAV date: {{ summary.portfolioDate }}
      highchart.col-span-3.m-2(:modules="['drilldown']" :options="pieOptions" @chartLoaded="pieChartLoaded")
    highstock.w-full(:options="options"
      :update="['options.title', 'options.series']"
      :animation="{duration: 1000}"
      @chartLoaded="chartLoaded")
    //DataView.mt-4(:value="schemes" layout="list")
      template(#header)
        //.grid.grid-cols-10.gap-4.p-4
          .col-span-2
            .flex.flex-col.items-center
              .text-xl.text-gray-500.font-medium.uppercase Current Value
              .text-2xl.font-medium {{ formatCurrency(totalValue) }}
          .col-span-2
            .flex.flex-col.items-center
              .text-lg.text-gray-500.font-medium Invested
              .text-base {{ formatCurrency(totalInvested) }}
          .col-span-2
            .flex.flex-col.items-center
              .text-lg.text-gray-500.font-medium Day Change
              .text-base {{ formatCurrency(totalChange) }}
          .col-span-2
            .flex.flex-col.items-center
              .text-lg.text-gray-500.font-medium Total Return
              .text-base {{ formatCurrency(totalValue - totalInvested) }}
          .col-span-2
            .flex.flex-col.items-center
              .text-lg.text-gray-500.font-medium Funds
              .text-base {{ schemes.length }}
        .grid.grid-cols-12.gap-4.p-4
          .col-span-6 Fund
          .col-span-2.text-right Value
          .col-span-2.text-right Invested
          .col-span-2.text-right Return
      template(#list="slotProps")
        .grid.grid-cols-12.gap-4.p-4
            .col-span-6
              .text-xl.capitalize.text-gray-500.font-medium {{ slotProps.data.name }}
              .grid.grid-cols-12
                .col-span-8
                  .flex.flex-row.items-center.my-2
                    .text-base.fonte-medium.text-gray-500 Units
                    .text-base.ml-2 {{ slotProps.data.units }}
                    .text-2xl.mx-2.text-gray-500.font-semibold •
                    ProgressBar.flex-grow(:value="100*slotProps.data.value/totalValue" style="height: 0.5em" :showValue="false")
                    .text-sm.text-left.ml-2 {{ (100*slotProps.data.value/totalValue).toFixed(2) }}%
              //.grid.grid-cols-12.my-2.items-center
                .col-span-12
                .text-sm.text-left {{ (100*slotProps.data.value/totalValue).toFixed(2) }}%
                ProgressBar(:value="100*slotProps.data.value/totalValue" style="height: 0.5em" :showValue="false")
                .text-lg.mx-2.text-gray-500.font-semibold •
                .text-sm Units {{slotProps.data.units}}
              //.flex.flex-row.items-center.my-2
                .flex.flex-row
                  .font-medium.text-base.text-gray-500 NAV
                  .text-base.ml-2 {{ slotProps.data.nav0 }}
                .text-2xl.mx-2.text-gray-500.font-semibold •
                .flex.flex-row
                  .font-medium.text-base.text-gray-500 Avg NAV
                  .text-base.ml-2 {{ slotProps.data.avg_nav }}
                .text-lg.mx-2.text-gray-500.font-semibold •
                .flex.flex-row
                  .font-medium.text-base.text-gray-500 1D Change
                  .text-base.ml-2 {{ formatCurrency(slotProps.data.change) }}
            .col-span-2
              .text-lg.text-right {{ formatCurrency(slotProps.data.value) }}
              .flex.flex-row.my-2.justify-end
                .flex.flex-row.items-center
                  .font-medium.text-xs.text-gray-500 NAV
                  .text-sm.ml-2 {{ slotProps.data.nav0 }}
            .col-span-2
              .text-lg.font-medium.text-right {{ formatCurrency(slotProps.data.invested) }}
              .flex.flex-row.my-2.justify-end
                .flex.flex-row.items-center
                  .font-medium.text-xs.text-gray-500 avg
                  .text-sm.ml-2 {{ slotProps.data.avg_nav }}
            .col-span-2
              .text-lg.text-right {{ formatCurrency(slotProps.data.value - slotProps.data.invested) }}
              .text-sm.text-right.my-2 {{ (100 * (slotProps.data.value - slotProps.data.invested)/slotProps.data.invested).toFixed(2) }}%
</template>

<script lang="ts">
import {
  defineComponent,
  onBeforeUnmount,
  onMounted,
  computed,
  reactive,
  ref,
  useNuxtApp,
} from "#imports";
import {
  DrilldownOptions,
  SeriesLineOptions,
  Options,
  SeriesPieOptions,
} from "highcharts";

import type { MFPortfolio, Scheme, Summary } from "~/definitions/mutualfunds";
import type { Chart } from "~/definitions/charts";
import { preparePieChartData } from "@/utils";
import type { AllocationPieChartData } from "@/utils";

export default defineComponent({
  setup() {
    const { $fetch, $emit } = useNuxtApp();

    const chart = ref<Chart | null>(null);
    const options = reactive<Options>({
      chart: {
        backgroundColor: "#edf0f5",
      },
      title: {
        text: "Portfolio Performance",
      },
      colors: [
        "#4CAF50",
        "#666666",
        "#058DC7",
        "#ED561B",
        "#DDDF00",
        "#24CBE5",
        "#64E572",
        "#FF9655",
        "#FFF263",
        "#6AF9C4",
      ],
      credits: {
        enabled: false,
      },
      lang: {
        thousandsSep: ",",
      },
      legend: {
        enabled: false,
      },
      navigator: {
        xAxis: {
          labels: {
            style: {
              fontWeight: "bold",
            },
          },
        },
      },
      plotOptions: {
        series: {
          animation: {
            duration: 1000,
          },
        },
      },
      rangeSelector: {
        allButtonsEnabled: true,
        buttonTheme: {
          fill: "none",
          stroke: "none",
          r: 3,
          style: {
            color: "#4CAF50",
            fontWeight: "bold",
          },
          states: {
            hover: {},
            select: {
              fill: "#4CAF50",
              style: {
                color: "white",
              },
            },
          },
        },
        inputStyle: {
          color: "#4CAF50",
          fontWeight: "bold",
        },
        selected: 4,
      },
      tooltip: {
        shared: true,
        useHTML: true,
      },
      xAxis: {
        labels: {
          style: {
            fontWeight: "bold",
          },
        },
      },
      yAxis: {
        labels: {
          style: {
            fontWeight: "bold",
          },
        },
      },
      series: [
        { name: "Current Value", data: [], type: "line" },
        { name: "Invested", data: [], type: "line" },
      ] as Array<SeriesLineOptions>,
      drilldown: {
        series: [],
      },
    });

    const pieChart = ref<Chart | null>(null);
    const pieOptions = reactive<Options>({
      chart: {
        backgroundColor: "#edf0f5",
        type: "pie",
      },
      colors: [
        "#4CAF50",
        "#666666",
        "#058DC7",
        "#ED561B",
        "#DDDF00",
        "#24CBE5",
        "#64E572",
        "#FF9655",
        "#FFF263",
        "#6AF9C4",
      ],
      credits: {
        enabled: false,
      },
      lang: {
        thousandsSep: ",",
      },
      legend: {
        enabled: false,
      },
      plotOptions: {
        series: {
          animation: {
            duration: 1000,
          },
          dataLabels: {
            enabled: true,
            format: "{point.name}: {point.y:.2f}%",
          },
        },
      },
      title: {
        text: "",
      },
      tooltip: {
        valueDecimals: 2,
        valueSuffix: "%",
      },
      series: [
        {
          name: "Investments",
          data: [],
          type: "pie",
        },
      ] as Array<SeriesPieOptions>,
      drilldown: {
        series: [],
      },
    });

    const portfolios = computed(() => []); // Replace with actual data fetching logic
    const currentPortfolio = computed(() => ({ id: -1 }));
    const selectedPortfolio = ref(currentPortfolio.value);

    const getPortfolio = async () => {
      // Replace with actual data fetching logic
    };

    const schemes = computed(() => []); // Replace with actual data fetching logic
    const summary = computed(() => ({})); // Replace with actual data fetching logic

    const schemesLoading = ref(false);
    const getSchemes = async (force = false) => {
      // Replace with actual data fetching logic
    };

    const init = async () => {
      await getPortfolio();
      await getSchemes();
    };

    onMounted(init);

    const formatCurrency = (num: Number) => {
      return num.toLocaleString("en-IN", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
        style: "currency",
        currency: "INR",
      });
    };

    const formatNumber = (num: number | null, digits = 2): string => {
      return num?.toFixed(digits) || "N.A.";
    };

    const formatPct = (num: number | null, digits = 2): string => {
      return formatNumber(num, digits) + " %";
    };

    const changePortfolio = async (portfolio: MFPortfolio) => {
      if (portfolio.id !== currentPortfolio.value.id) {
        await getPortfolio();
        await getSchemes(true);
      }
    };

    return {
      options,
      pieOptions,
      schemes,
      portfolios,
      currentPortfolio,
      selectedPortfolio,
      formatCurrency,
      formatNumber,
      formatPct,
      summary,
      changePortfolio,
    };
  },
});
</script>

<style lang="scss">
@use "sass:color";
@use "assets/layout/_variables" as variables;

.summary-title-main {
  @apply text-sm w-full text-white text-center;
}
.summary-value-main {
  @apply text-2xl text-white text-center font-bold;
}

.summary-title-sub {
  @apply text-base w-full text-white text-center;
}
.summary-value-sub {
  @apply text-xl w-full text-white text-center;
}

.p-dataview {
  .p-dataview-content {
    background: variables.$bodyBgColor;

    > .p-grid > div {
      @apply border-gray-400;
    }
  }
  .p-dataview-header {
    background: color.adjust(variables.$bodyBgColor, $lightness: -2%);
  }
}
.highcharts-loading {
  opacity: 1 !important;
  background: #edf0f5 !important;
}

.highcharts-loading-inner,
.highcharts-loading-inner::before,
.highcharts-loading-inner::after {
  background: #4caf50;
  -webkit-animation: load1 1s infinite ease-in-out;
  animation: load1 1s infinite ease-in-out;
  width: 1em;
  height: 4em;
}
.highcharts-loading-inner {
  display: block;
  color: #4caf50;
  text-indent: -9999em;
  margin: 0 auto;
  top: 50% !important;
  position: relative;
  font-size: 11px;
  -webkit-transform: translate3d(-50%, -50%, 0);
  -ms-transform: translate3d(-50%, -50%, 0);
  transform: translate3d(-50%, -50%, 0);
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}
.highcharts-loading-inner::before,
.highcharts-loading-inner::after {
  position: absolute;
  top: 0;
  content: "";
}
.highcharts-loading-inner::before {
  left: -1.5em;
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}
.highcharts-loading-inner::after {
  left: 1.5em;
}
@-webkit-keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}
@keyframes load1 {
  0%,
  80%,
  100% {
    box-shadow: 0 0;
    height: 4em;
  }
  40% {
    box-shadow: 0 -2em;
    height: 5em;
  }
}

.summary.p-card {
  @apply rounded-xl bg-gradient-to-tr from-gray-900 to-gray-500;

  color: white;
}

body {
  background: color.adjust(variables.$bodyBgColor, $lightness: -2%);
}
</style>
